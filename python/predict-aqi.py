# coding=utf-8
import numpy as np
from sklearn.externals import joblib
import threading
import datetime


def build_data(x):
    test_x, m = [], 7
    for i in range(len(x)-m):
        test_x.append(np.reshape(x[i:i+m], (49,)))
    return np.array(test_x)


def predict(path, model, x, result):
    mo = joblib.load(path + model)
    y_ = mo.predict(x)
    result.append(y_)


def index_data(predict_data, path):
    x = []
    date = []
    for r in predict_data.split("\n"):
        r = r.split(",")
        date.append(r[0][:10])
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    predict_days = 7
    aqi = x[-predict_days:, 0]
    test_x = build_data(x)

    test_x = test_x[-1].reshape(1, 49)
    date = date[-predict_days:]
    for i in range(predict_days):
        now = datetime.datetime.strptime(date[-1], "%Y-%m-%d")
        date.append("{0}".format(now + datetime.timedelta(days=1))[:10])

    # lr
    lr_result = []
    t = threading.Thread(target=predict, args=(path, "lr.pkl", test_x, lr_result))
    t.start()
    t.join()

    # nn
    nn_result = []
    t = threading.Thread(target=predict, args=(path, "bp.pkl", test_x, nn_result))
    t.start()
    t.join()
    lr_result = lr_result[0][0]
    lr_result[0] = nn_result[0][0]
    res = "{0}\n{1}\n{2}".format(",".join(date),
                                           ",".join(aqi.astype(np.str)),
                                           ",".join(lr_result.astype(np.str)))
    return res


# if __name__ == "__main__":
#     data = open("/Users/quietsj/go/src/air-quality-predict/docs/aqi-data.csv", "r")
#     index_data(data.read(), "/Users/quietsj/go/src/air-quality-predict/docs/")
