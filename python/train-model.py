# coding:utf-8
import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, make_scorer, explained_variance_score, r2_score
import threading
import time
import pandas as pd
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


def l1_loss(y, y_):
    return np.mean(map(abs, y - y_))


def mean_relative_error(y_true, y_pred):
    return np.mean(map(abs, (y_true - y_pred) / y_true))


def calculate_loss(path, model, x, y, result):
    mo = joblib.load(path + model)
    y_ = mo.predict(x)
    result.append(l1_loss(y, y_))


def fit(mo, path, train_x, train_y):
    mo.fit(train_x, train_y)
    joblib.dump(mo, path)


def normal(x):
    x = pd.DataFrame(x)
    x = (x - x.min()) / (x.max() - x.min())
    # x = (x - x.mean()) / x.std()
    x.dropna(axis=1, how="any", inplace=True)
    x = x.values
    return x
    pca = PCA(n_components=1, copy=False, svd_solver="full")
    pca.fit(x)
    return pca.transform(x)


def build_model(path, train_x, train_y, validate_x, validate_y, mo, name):
    # normal(train_x)
    # normal(validate_x)
    # t = threading.Thread(target=fit, args=(mo, path + name + ".pkl", train_x, train_y))
    # t.start()
    # t.join()
    # return
    # result = []
    # t = threading.Thread(target=calculate_loss, args=(path, name + ".pkl", train_x, train_y, result))
    # t.start()
    # t.join()
    # print name + " train", np.mean(result)
    # result = []
    # t = threading.Thread(target=calculate_loss, args=(path, name + ".pkl", validate_x, validate_y, result))
    # t.start()
    # t.join()
    # print name + " valid", np.mean(result)

    # param_grid = {
    #     "loss": ["lad"],
    #     "min_samples_split": [2, 4],
    #     "min_samples_leaf": [1, 2],
    #     "max_depth": [2, 3, 4, 5],
    #     "max_features": [7, 14],
    # }
    # grid_search = GridSearchCV(
    #     estimator=GradientBoostingRegressor(),
    #     param_grid=param_grid,
    #     cv=5,
    #     scoring=make_scorer(explained_variance_score)
    # )
    # grid_search.fit(train_x, train_y)
    #
    # best_model = grid_search.best_estimator_
    # best_model.fit(train_x, train_y)
    # print grid_search.best_params_, grid_search.best_score_
    # print "mean absolute error:", mean_absolute_error(validate_y, best_model.predict(validate_x))
    # print "mean relative error:", mean_relative_error(validate_y, best_model.predict(validate_x))
    # return

    from keras.layers import Input, Dense, regularizers
    from keras.models import Model, load_model
    from keras import optimizers, losses
    from keras.callbacks import EarlyStopping

    # train_x = normal(train_x)
    # validate_x = normal(validate_x)

    # for j in range(49):
    #     train_j = pd.Series(train_x[:, j])
    #     valid_j = pd.Series(validate_x[:, j])
    #     print train_j.corr(pd.Series(train_y)), valid_j.corr(pd.Series(validate_y))
    # exit(1)

    # inputs = Input(shape=(49,))
    # x = Dense(1, activation="linear")(inputs)
    # predictions = Dense(1, activation="linear")(x)
    #
    # model = Model(inputs=inputs, outputs=predictions)
    # model.compile(optimizer=optimizers.Adam(decay=1e-7),
    #               loss=losses.mean_absolute_error)
    # batch_size = 128
    # early_stopping = EarlyStopping(monitor="val_loss", patience=20)
    # history = model.fit(train_x, train_y, batch_size=batch_size, epochs=600,
    #                     validation_data=(validate_x, validate_y), verbose=0, callbacks=[early_stopping])
    # model.save("./docs/model.h5")

    # lr = LinearRegression()
    # knn = KNeighborsRegressor(n_neighbors=18)
    # svr = SVR(kernel="rbf", C=1000, gamma=1e-6)
    # gbdt = GradientBoostingRegressor(loss="lad", min_samples_split=4, min_samples_leaf=2,
    #                                  max_depth=4, max_features=14)
    # lr.fit(train_x, train_y)
    # knn.fit(train_x, train_y)
    # svr.fit(train_x, train_y)
    # gbdt.fit(train_x, train_y)
    # joblib.dump(lr, "./docs/LR.pkl")
    # joblib.dump(knn, "./docs/KNN.pkl")
    # joblib.dump(svr, "./docs/SVR.pkl")
    # joblib.dump(gbdt, "./docs/GBDT.pkl")

    matx = np.mat(np.hstack((train_x, np.ones(1740).reshape(1740, 1))))
    print np.linalg.matrix_rank(matx.T * matx)
    lr = joblib.load("./docs/LR.pkl")
    knn = joblib.load("./docs/KNN.pkl")
    svr = joblib.load("./docs/SVR.pkl")
    gbdt = joblib.load("./docs/GBDT.pkl")
    model = load_model("./docs/model.h5")

    days = range(1, 29)
    for day in [28]:
        lr_mae = lr.predict(validate_x[:day])
        knn_mae = knn.predict(validate_x[:day])
        svr_mae = svr.predict(validate_x[:day])
        gbdt_mae = gbdt.predict(validate_x[:day])
        model_mae = model.predict(validate_x[:day])
    # plt.plot(days, lr_mae, "o-", color="green")
    # plt.plot(days, knn_mae, "o-", color="peru")
    # plt.plot(days, svr_mae, "o-", color="blue")
    # plt.plot(days, gbdt_mae, "o-", color="red")
    # plt.plot(days, model_mae, "o-", color="purple")
    # plt.plot(days, validate_y[:day], "o-", color="black")
    # plt.title("Predict 28 Days")
    # plt.ylabel("AQI")
    # plt.xlabel("Future Day")
    # plt.legend(["SVR", "Real"], loc='upper left')
    # plt.show()
    # plt.savefig("./images/predict-28-days.jpg")

    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('Model loss')
    # plt.ylabel('Loss')
    # plt.xlabel('Epoch')
    # plt.legend(['Train', 'Valid'], loc='upper left')
    # # plt.show()
    # plt.savefig("./images/model-loss.jpg")


def build_data(x, m):
    train_x, train_y, y_num= [], [], 7
    for i in range(len(x)-m-y_num):
        train_x.append(np.reshape(x[i:i+m, :], (7*m,)))
        train_y.append(x[i+m:i+m+y_num, 0])
    return np.array(train_x), np.array(train_y)


def train(train_data, path):
    start = time.time()
    x = []
    date = []
    for r in train_data.split("\n"):
        r = r.split(",")
        date.append(r[0])
        x.append(r[1:2] + r[3:])
    x = np.array(x).astype(np.float64)
    train_x, train_y = build_data(x, 7)
    validate_x = train_x[-100:]
    validate_y = train_y[-100:]
    train_x = train_x[:-100]
    train_y = train_y[:-100]
    build_model(path, train_x, train_y, validate_x, validate_y,
                LinearRegression(), "lr")
    # build_model(path, train_x, train_y[:, 0], validate_x, validate_y[:, 0],
    #             MLPRegressor(hidden_layer_sizes=(1, ), max_iter=10000, activation="identity"), "bp")
    # return "{0} s finish train".format(time.time() - start)


if __name__ == "__main__":
    data = open("/Users/quietsj/go/src/air-quality-predict/docs/aqi-data.csv", "r")
    train(data.read(), "/Users/quietsj/go/src/air-quality-predict/docs/")


# mean:15.16, np.mean([abs(x[i+1, 0] - x[i, 0]) for i in range(len(x)-1)])
# std:26.84, np.std(x[:, 0])
# AQI PM2.5 PM10 SO2 CO	NO2	O3
