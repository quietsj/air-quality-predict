# coding=utf-8
import numpy as np
from sklearn.externals import joblib
import json
import threading
import datetime


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))


def build_train_data(data, date, m):
    x = []
    label = []
    y_date = []
    for i in range(len(data)-m):
        x.append(data[i:i+m])
        label.append(data[i+m])
        y_date.append(date[i+m][:10])
    return np.array(x), np.array(label), ",".join(y_date)


def predict(path, test_x, y, model):
    mo = joblib.load(path + model)
    y["result"] = np.around(mo.predict(test_x), decimals=1)


def get_compare(predict_data, path, model_name):
    with open(path + "train-model.json", 'r') as f:
        train_model_json = json.load(f)
    x = []
    date = []
    for r in predict_data.split("\n"):
        r = r.split(",")
        date.append(r[0])
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    aqi = x[:, 0]
    aqi_diff = train_model_json["aqi_max"] - train_model_json["aqi_min"]
    aqi = (aqi - train_model_json["aqi_min"]) / aqi_diff

    aqi_x, aqi_label, y_date = build_train_data(aqi, date, train_model_json["{0}_m".format(model_name)])
    y = {}
    t = threading.Thread(target=predict, args=(path, aqi_x, y, "{0}.pkl".format(model_name)))
    t.start()
    t.join()
    aqi_label = aqi_label * aqi_diff + train_model_json["aqi_min"]
    y = y["result"] * aqi_diff + train_model_json["aqi_min"]
    return ",".join(y.astype(np.str)) + "\n" + ",".join(aqi_label.astype(np.str)) + "\n" + y_date


def nearest_neighbors(predict_data, path):
    return get_compare(predict_data, path, "knn")


def gradient_boosting_tree(predict_data, path):
    return get_compare(predict_data, path, "gbdt")


def index_data(predict_data, path):
    with open(path + "train-model.json", 'r') as f:
        train_model_json = json.load(f)
    x = []
    date = []
    for r in predict_data.split("\n"):
        r = r.split(",")
        date.append(r[0])
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    aqi = x[:, 0]
    aqi_diff = train_model_json["aqi_max"] - train_model_json["aqi_min"]
    aqi = list((aqi - train_model_json["aqi_min"]) / aqi_diff)
    predict_days = 7
    for i in range(predict_days):
        now = datetime.datetime.strptime(date[-1][:10], "%Y-%m-%d")
        date.append("{0}".format(now + datetime.timedelta(days=1)))
    gbdt_m = train_model_json["gbdt_m"]
    for i in range(predict_days):
        y_ = {}
        t = threading.Thread(target=predict,
                             args=(path,
                                   np.array(aqi[-gbdt_m:]).reshape(1, gbdt_m),
                                   y_, "gbdt.pkl"))
        t.start()
        t.join()
        if i > 0:
            aqi.append(y_["result"][0] + 0.01 * np.random.randint(-5, 6))
        else:
            aqi.append(y_["result"][0])
    aqi = np.array(aqi) * aqi_diff + train_model_json["aqi_min"]
    date = [day[:10] for day in date]
    return ",".join(date) + "\n" + ",".join(aqi.astype(np.str))

