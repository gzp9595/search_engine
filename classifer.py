import time
from sklearn import metrics
import pickle as pickle
import config
import os
import json
import ranking


# Multinomial Naive Bayes Classifier  
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier  
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier  
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier  
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier  
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier  
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier  
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model


# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs=1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in list(best_parameters.items()):
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model


classifiers = {'NB': naive_bayes_classifier,
               'KNN': knn_classifier,
               'LR': logistic_regression_classifier,
               'RF': random_forest_classifier,
               'DT': decision_tree_classifier,
               'SVM': svm_classifier,
               'SVMCV': svm_cross_validation,
               'GBDT': gradient_boosting_classifier
               }

use_what = "GBDT"


class model:
    def load_model(self):
        self.models = pickle.load(open(config.MODEL_FILE, 'r'))

    def train_model(self, X, Y):
        self.models = classifiers[use_what](X, Y)

    def save_model(self):
        pickle.dump(self.models, open(config.MODEL_FILE, "wb"))

    def judge(self, X):
        return self.models.predict(X)


if __name__ == "__main__":
    X = []
    Y = []
    models = model();
    for x in os.listdir(config.TRAINING_DIR):
        f = open(config.TRAINING_DIR + x, "r")
        content = ''
        for line in f:
            content = json.loads(line)
            break

        X.append(ranking.get_feature(content["obj"], content["query"]))
        Y.append(content["score"])

    models.train_model(X,Y)
    models.save_model()
