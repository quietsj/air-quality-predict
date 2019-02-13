import numpy as np
from sklearn.externals import joblib
import json
import threading


def nearest_neighbors(predict_data, path):
    with open(path + "train-model.json", 'r') as f:
        d = json.load(f)
    x = []
    date = []
    for r in predict_data.split("\n"):
        r = r.split(",")
        date.append(r[0])
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    aqi = x[:, 0]
    aqi_x, aqi_label, y_date = build_train_data(aqi, date, d["knn_m"])
    y = {}
    t = threading.Thread(target=predict, args=(path, aqi_x, y))
    t.start()
    t.join()
    return ",".join(y["result"].astype(np.str)) + "\n" + ",".join(aqi_label.astype(np.str)) + "\n" + y_date


def build_train_data(data, date, m):
    x = []
    label = []
    y_date = []
    for i in range(len(data)-m):
        x.append(data[i:i+m])
        label.append(data[i+m])
        y_date.append(date[i+m][:10])
    return np.array(x), np.array(label), ",".join(y_date)


def predict(path, test_x, y):
    mo = joblib.load(path + "knn.pkl")
    y["result"] = np.around(mo.predict(test_x), decimals=1)

