import numpy as np
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.externals import joblib
import threading
import json


def train(train_data, path):
    x = []
    for r in train_data.split("\n"):
        r = r.split(",")
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    nearest_neighbors(x, path)


def nearest_neighbors(x, path):
    aqi = x[:, 0]
    losses = []
    for m in range(1, 10):
        for k in range(1, 10):
            aqi_x, aqi_label = build_train_data(aqi, m)
            loss = cross_val(KNeighborsRegressor(n_neighbors=k, weights="distance", metric="euclidean"), aqi_x, aqi_label)
            losses.append((loss, m, k))
    loss, m, k = min(losses)
    mo = KNeighborsRegressor(n_neighbors=k, weights="distance", metric="euclidean")
    aqi_x, aqi_label = build_train_data(aqi, m)
    t = threading.Thread(target=fit, args=(mo, path + "knn.pkl", aqi_x, aqi_label))
    t.start()
    t.join()
    d = {"knn_m": m}
    with open(path + "train-model.json", "w") as f:
        json.dump(d, f)


def fit(mo, path, train_x, train_y):
    mo.fit(train_x, train_y)
    joblib.dump(mo, path)
    

def build_train_data(data, m):
    x = []
    label = []
    for i in range(len(data)-m):
        x.append(data[i:i+m])
        label.append(data[i+m])
    return np.array(x), np.array(label)


def cross_val(mo, x, y):
    kf = KFold(n_splits=10, shuffle=True)
    result = []
    for train_index, test_index in kf.split(x):
        train_x = x[train_index]
        train_y = y[train_index]
        test_x = x[test_index]
        test_y = y[test_index]
        t = threading.Thread(target=get_loss, args=(mo, train_x, train_y, test_x, test_y, result))
        t.start()
        t.join()
    return np.mean(result)


def get_loss(mo, train_x, train_y, test_x, test_y, result):
    mo.fit(train_x, train_y)
    y_ = mo.predict(test_x)
    result.append(l1_loss(test_y, y_))


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))

