import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import datasets
from sklearn.model_selection import train_test_split

# data = datasets.load_iris()
# X = data.data
# y = data.target
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=20)
# clf = svm.SVC(kernel="linear", C=1e5, decision_function_shape="ovo")
# clf.fit(X_train, y_train)
#
# y_pred = clf.predict(X_test)
# print(accuracy_score(y_test, y_pred) * 100)

dic = [1, 2, 3, 4, 5]
