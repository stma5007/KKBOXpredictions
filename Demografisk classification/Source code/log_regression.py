# imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import statsmodels.api as sm
from scipy import stats

all_features = ["dots","exclmark","questionmark","commas", "spaces", "wes", "America",
              "war", "terrorism", "a", "b", "c", "d", "e", "ed", "will", "russia",
              "bomb", "great", "family", "happy", "child", "peace", "enemy",
              "soldier","excuse","letters", "punctuation", "flesch_read", "smog_read",
              "verb_count", "adjektiv_count", "pronoun_count"]

democrat_list = ["exclmark","questionmark","commas", "spaces", "wes", "America",
              "war", "terrorism", "a", "e", "ed", "will", "russia",
              "bomb", "great", "happy", "child",
              "letters", "punctuation", "flesch_read", "smog_read",
              "verb_count", "adjektiv_count", "pronoun_count"]

cheater_list = ["exclmark","questionmark","commas", "wes",
              "war", "a", "b", "d", "e", "ed", "will", "russia",
              "bomb", "family", "happy", "child",
              "letters", "punctuation", "flesch_read", "smog_read",
              "pronoun_count"]

wartime_list = ["commas", "spaces", "America",
              "war", "terrorism", "a", "c", "e", "will",
              "bomb", "great", "child", "peace", "enemy",
              "soldier","excuse","letters", "punctuation",
              "verb_count", "pronoun_count"]

assassinated_list = ["commas", "wes", "America",
              "a", "b", "c", "d", "e", "russia",
              "bomb", "great", "family", "happy", "child",
              "letters", "punctuation", "smog_read",
              "adjektiv_count", "pronoun_count"]

def load_data():
    dataset = pd.read_csv("/home/gregkoncz/git/FYP_miniprojekt3/data/all_speech_data/all_speeches_measures.csv")
    return dataset

def log_reg_with_statmodels(data, target):
    data.dropna(inplace = True)
    if target == "democrat":
        X = data[democrat_list]
    elif target == "cheater":
        X = data[cheater_list]
    elif target == "war_time":
        X = data[wartime_list]
    elif target == "assassinated":
        X = data[assassinated_list]
    else:
        X = data[all_features]
    Y = data[target]
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
    logit_model = sm.Logit(Y, X)
    result = logit_model.fit()
    print(result.summary())
    predictions = result.predict()
    print(len(predictions))
    print(len(X))
    nominal_predictions = [0 if x < 0.5 else 1 for x in predictions]
    print(confusion_matrix(Y, nominal_predictions))
    print(accuracy_score(Y, nominal_predictions))
    #predictions = result.predict(X_test)
    #print(accuracy_score(y_test, predictions))

def log_regression(data, target):
    data.dropna(inplace = True)
    if target == "democrat":
        X = data[democrat_list]
    elif target == "cheater":
        X = data[cheater_list]
    elif target == "war_time":
        X = data[wartime_list]
    else:
        X = data[all_features]
    Y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    this_accuracy_score = accuracy_score(y_test, predictions)
    print(this_accuracy_score)
    print(model.coef_)
    print(confusion_matrix(y_test, predictions))

def naive_classifier(data, target):
    X = data[["dots", "exclmark", "questionmark", "commas", "spaces", "Is", "wes", "America", "war", "terrorism",
              "a", "b", "c", "d", "e", "ed", "will", "russia", "bomb", "great", "letters", "punctuation"]]
    Y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
    model = GaussianNB()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    this_accuracy_score = accuracy_score(y_test, predictions)
    print(this_accuracy_score)
    #print(model.coef_)

def knn_classifier(data, target, neighbors):
    X = data[["dots", "exclmark", "questionmark", "commas", "spaces", "Is", "wes", "America", "war", "terrorism",
              "a", "b", "c", "d", "e", "ed", "will", "russia", "bomb", "great", "letters", "punctuation"]]
    Y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
    model = KNeighborsClassifier(n_neighbors = neighbors)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    this_accuracy_score = accuracy_score(y_test, predictions)
    print(this_accuracy_score)
    #print(model.coef_)

def multiclass_regression_for_historics(data):
    X = data[["dots", "exclmark", "questionmark", "commas", "spaces", "Is", "wes", "America", "war", "terrorism",
              "a", "b", "c", "d", "e", "ed", "will", "russia", "bomb", "great", "letters", "punctuation"]]
    Y = data["historical_period"]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    this_accuracy_score = accuracy_score(y_test, predictions)
    print(this_accuracy_score)
    print(model.coef_)

if __name__ == '__main__':

    data = load_data()
    #log_regression(data, "cheater")
    #log_regression(data, "democrat")
    #log_regression(data, "war_time")
    #multiclass_regression_for_historics(data)
    #knn_classifier(data, "cheater", 3)
    #knn_classifier(data, "democrat", 3)
    #naive_classifier(data, "war_time")
    log_reg_with_statmodels(data = data, target = "assassinated")
