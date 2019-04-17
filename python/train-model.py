import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
import threading
import time


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))


def calculate_loss(path, model, x, y, result):
    mo = joblib.load(path + model)
    y_ = mo.predict(x)
    result.append(l1_loss(y, y_))


def fit(mo, path, train_x, train_y):
    mo.fit(train_x, train_y)
    joblib.dump(mo, path)


def normal(x):
    for j in range(x.shape[1]):
        seq = x[:, j]
        x[:, j] = (seq - np.min(seq)) / (np.max(seq) - np.min(seq))


def build_model(path, train_x, train_y, validate_x, validate_y, mo, name):
    # normal(train_x)
    # normal(validate_x)
    t = threading.Thread(target=fit, args=(mo, path + name + ".pkl", train_x, train_y))
    t.start()
    t.join()
    result = []
    t = threading.Thread(target=calculate_loss, args=(path, name + ".pkl", train_x, train_y, result))
    t.start()
    t.join()
    print name + " train", np.mean(result)
    result = []
    t = threading.Thread(target=calculate_loss, args=(path, name + ".pkl", validate_x, validate_y, result))
    t.start()
    t.join()
    print name + " valid", np.mean(result)


def build_data(x):
    train_x, train_y, y_num, m = [], [], 7, 7
    for i in range(len(x)-m-y_num):
        train_x.append(np.reshape(x[i:i+m, :], (7*m,)))
        train_y.append(x[i+m:i+m+y_num, 0])
    return np.array(train_x), np.array(train_y)


def train(train_data, path):
    start = time.time()
    x = []
    for r in train_data.split("\n"):
        r = r.split(",")
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    train_x, train_y = build_data(x)
    validate_x = train_x[-100:]
    validate_y = train_y[-100:]
    train_x = train_x[:-100]
    train_y = train_y[:-100]
    build_model(path, train_x, train_y, validate_x, validate_y,
                LinearRegression(), "lr")
    build_model(path, train_x, train_y[:, 0], validate_x, validate_y[:, 0],
                MLPRegressor(hidden_layer_sizes=(1, ), max_iter=10000, activation="identity"), "bp")
    return "{0} s finish train".format(time.time() - start)


# if __name__ == "__main__":
#     data = open("/Users/quietsj/go/src/air-quality-predict/docs/aqi-data.csv", "r")
#     train(data.read(), "")


# mean:15.16, np.mean([abs(x[i+1, 0] - x[i, 0]) for i in range(len(x)-1)])
# std:26.84, np.std(x[:, 0])
# AQI PM2.5 PM10 SO2 CO	NO2	O3
