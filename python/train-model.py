import numpy as np
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib
import threading
import json
import time


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))


def get_loss(mo, train_x, train_y, test_x, test_y, result):
    mo.fit(train_x, train_y)
    y_ = mo.predict(test_x)
    result.append(l1_loss(test_y, y_))


def cross_val(mo, x, y):
    kf = KFold(n_splits=10, shuffle=True)
    result = []
    ts = []
    for train_index, test_index in kf.split(x):
        train_x = x[train_index]
        train_y = y[train_index]
        test_x = x[test_index]
        test_y = y[test_index]
        t = threading.Thread(target=get_loss, args=(mo, train_x, train_y, test_x, test_y, result))
        t.start()
        ts.append(t)
    for t in ts:
        t.join()
    return np.mean(result)


def build_train_data(data, m):
    x = []
    label = []
    for i in range(len(data)-m):
        x.append(data[i:i+m])
        label.append(data[i+m])
    return np.array(x), np.array(label)


def fit(mo, path, train_x, train_y):
    mo.fit(train_x, train_y)
    joblib.dump(mo, path)


def normalize(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())


def normalize_merge(x, m):
    for i in range(x.shape[1]):
        if i == 0:
            merge_x, merge_y = build_train_data(normalize(x[:, i]), m)
        else:
            bx, by = build_train_data(normalize(x[:, i]), m)
            merge_x = np.vstack((merge_x, bx))
            merge_y = np.hstack((merge_y, by))
    return merge_x, merge_y


def nearest_neighbors(x, path, train_model_json):
    losses = []
    for m in range(1, 10):
        for k in range(1, 10):
            merge_x, merge_y = normalize_merge(x, m)
            loss = cross_val(KNeighborsRegressor(n_neighbors=k, weights="distance", metric="euclidean"),
                             merge_x, merge_y)
            losses.append((loss, m, k))

    loss, great_m, k = min(losses)
    mo = KNeighborsRegressor(n_neighbors=k, weights="distance", metric="euclidean")
    merge_x, merge_y = normalize_merge(x, great_m)
    t = threading.Thread(target=fit, args=(mo, path + "knn.pkl", merge_x, merge_y))
    t.start()
    t.join()
    train_model_json["knn_m"] = great_m


def gradient_boosting_tree(x, path, train_model_json):
    great_m = 7
    mo = GradientBoostingRegressor(loss="lad")
    merge_x, merge_y = normalize_merge(x, great_m)
    t = threading.Thread(target=fit, args=(mo, path + "gbdt.pkl", merge_x, merge_y))
    t.start()
    t.join()
    train_model_json["gbdt_m"] = great_m


def save_max_and_min(x, d):
    aqi = x[:, 0]
    pm2_5 = x[:, 1]
    pm10 = x[:, 2]
    so2 = x[:, 3]
    co = x[:, 4]
    no2 = x[:, 5]
    o3_8h = x[:, 6]
    d["aqi_max"] = aqi.max()
    d["aqi_min"] = aqi.min()
    d["pm2_5_max"] = pm2_5.max()
    d["pm2_5_min"] = pm2_5.min()
    d["pm10_max"] = pm10.max()
    d["pm10_min"] = pm10.min()
    d["so2_max"] = so2.max()
    d["so2_min"] = so2.min()
    d["co_max"] = co.max()
    d["co_min"] = co.min()
    d["no2_max"] = no2.max()
    d["no2_min"] = no2.min()
    d["o3_8h_max"] = o3_8h.max()
    d["o3_8h_min"] = o3_8h.min()


def train(train_data, path):
    start = time.time()
    x, train_model_json = [], {}
    for r in train_data.split("\n"):
        r = r.split(",")
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    save_max_and_min(x, train_model_json)

    nearest_neighbors(x, path, train_model_json)
    gradient_boosting_tree(x, path, train_model_json)
    with open(path + "train-model.json", "w") as f:
         json.dump(train_model_json, f)
    return "{0} s finish train".format(time.time() - start)


