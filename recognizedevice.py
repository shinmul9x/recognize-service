import pandas as pd
import numpy as np
from sklearn import svm

model = svm.SVC(decision_function_shape='ovr', C=1e5, kernel='linear')
trained = False


def load_data(file_name):
    data = pd.read_csv(file_name, header=None)
    x = data.iloc[:, :20].to_numpy()
    y = data[20].to_numpy()
    return x, y


def train_model():
    x_train, y_train = load_data('data_train.csv')
    model.fit(x_train, y_train)

    x_test, y_test = load_data('data_test.csv')
    model.predict(x_test)
    global trained
    trained = True


def recognize_device(x):
    if not trained:
        return 'model has never been trained'
    return model.predict(np.reshape(np.array(x), (1, 20))).tolist()[0]
