# coding=utf-8
import numpy as np
from sklearn.externals import joblib
import threading
import datetime


def normal(x):
    for j in range(x.shape[1]):
        sea = x[:, j]
        x[:, j] = (sea - np.mean(sea)) / np.std(sea)


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
    normal(test_x)

    test_x = test_x[-1].reshape(1, 49)
    date = date[-predict_days:]
    for i in range(predict_days):
        now = datetime.datetime.strptime(date[-1], "%Y-%m-%d")
        date.append("{0}".format(now + datetime.timedelta(days=1))[:10])
    # knn
    knn_result = []
    t = threading.Thread(target=predict, args=(path, "knn.pkl", test_x, knn_result))
    t.start()
    t.join()
    # gbdt
    gbdt_result = []
    for j in range(predict_days):
        gbdtj_result = []
        t = threading.Thread(target=predict, args=(path, "gbdt{0}.pkl".format(j),
                                                          test_x, gbdtj_result))
        t.start()
        t.join()
        gbdt_result.append(gbdtj_result[0][0])
    gbdt_result = np.array(gbdt_result)
    # nn
    nn_result = []
    t = threading.Thread(target=predict, args=(path, "nn.pkl", test_x, nn_result))
    t.start()
    t.join()
    res = "{0}\n{1}\n{2}\n{3}\n{4}".format(",".join(date),
                                           ",".join(aqi.astype(np.str)),
                                           ",".join(knn_result[0][0].astype(np.str)),
                                           ",".join(gbdt_result.astype(np.str)),
                                           ",".join(nn_result[0][0].astype(np.str)))
    return res


# if __name__ == "__main__":
#     data = open("/Users/quietsj/go/src/air-quality-predict/docs/aqi-data.csv", "r")
#     index_data(data.read(), "/Users/quietsj/go/src/air-quality-predict/docs/")
