import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import threading
import time


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))


def normal(x):
    for j in range(x.shape[1]):
        sea = x[:, j]
        x[:, j] = (sea - np.mean(sea)) / np.std(sea)


def calculate_loss(path, model, x, y, result):
    mo = joblib.load(path + model)
    y_ = mo.predict(x)
    result.append(l1_loss(y, y_))


def fit(mo, path, train_x, train_y):
    mo.fit(train_x, train_y)
    joblib.dump(mo, path)


def nearest_neighbors(path, train_x, train_y, validate_x, validate_y):
    mo = KNeighborsRegressor(n_neighbors=7)
    normal(train_x)
    normal(validate_x)
    t = threading.Thread(target=fit, args=(mo, path + "knn.pkl", train_x, train_y))
    t.start()
    t.join()
    result = []
    t = threading.Thread(target=calculate_loss, args=(path, "knn.pkl", validate_x, validate_y, result))
    t.start()
    t.join()
    print "knn", np.mean(result)


def gradient_boosting_tree(path, train_x, train_y, validate_x, validate_y):
    mo = GradientBoostingRegressor(n_estimators=200, max_features=14, max_depth=7,
                                   learning_rate=0.01, loss="lad")
    normal(train_x)
    normal(validate_x)
    for j in range(train_y.shape[1]):
        t = threading.Thread(target=fit, args=(mo, path + "gbdt{0}.pkl".format(j),
                                               train_x, train_y[:, j]))
        t.start()
        t.join()
    result = []
    for j in range(train_y.shape[1]):
        t = threading.Thread(target=calculate_loss, args=(path, "gbdt{0}.pkl".format(j),
                                                          validate_x, validate_y[:, j], result))
        t.start()
        t.join()
    print "gbdt", np.mean(result)


def neural_network(path, train_x, train_y, validate_x, validate_y):
    mo = MLPRegressor(hidden_layer_sizes=(2, 3), alpha=0.1,
                      max_iter=10000, activation="tanh")
    normal(train_x)
    normal(validate_x)
    t = threading.Thread(target=fit, args=(mo, path + "nn.pkl", train_x, train_y))
    t.start()
    t.join()
    result = []
    t = threading.Thread(target=calculate_loss, args=(path, "nn.pkl", validate_x, validate_y, result))
    t.start()
    t.join()
    print "nn valid", np.mean(result)


def build_data(x):
    train_x, train_y, m = [], [], 7
    for i in range(len(x)-m-7):
        train_x.append(np.reshape(x[i:i+m], (49,)))
        train_y.append(x[i+m:i+m+7, 0])
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
    nearest_neighbors(path, train_x, train_y, validate_x, validate_y)
    gradient_boosting_tree(path, train_x, train_y, validate_x, validate_y)
    neural_network(path, train_x, train_y, validate_x, validate_y)
    return "{0} s finish train".format(time.time() - start)


# if __name__ == "__main__":
#     data = open("/Users/quietsj/go/src/air-quality-predict/docs/aqi-data.csv", "r")
#     train(data.read(), "")


