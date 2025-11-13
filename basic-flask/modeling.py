import pandas as pd
import sklearn as sklearn
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def load_data(path):
    print(f"Loading data from {path}")
    data = pd.read_csv(path)
    print(data.head())
    return data

def preprocess_data(df):
    print("Preprocessing data")
    # Filling missing values
    df.replace("?", np.nan, inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)  # Fill missing values with the mode

    # Discretization (simplifying marital status)
    df.replace(['Divorced', 'Married-AF-spouse', 'Married-civ-spouse', 
            'Married-spouse-absent', 'Never-married', 'Separated', 'Widowed'],
           ['divorced', 'married', 'married', 'married', 
            'not married', 'not married', 'not married'], inplace=True)

    # Label Encoding
    category_col = ['workclass', 'race', 'education', 'marital-status', 'occupation',
                    'relationship', 'gender', 'native-country', 'income']
    label_encoder = sklearn.preprocessing.LabelEncoder()

    # Creating a mapping dictionary
    mapping_dict = {}
    for col in category_col:
        df[col] = label_encoder.fit_transform(df[col])
        mapping_dict[col] = dict(enumerate(label_encoder.classes_))  # Improved mapping

    print(mapping_dict)

    # Dropping redundant columns
    df.drop(['fnlwgt', 'educational-num'], axis=1, inplace=True)
    print(f"Data after preprocessing: {df.head()}")

    return df

def train_model(df):

    # Splitting features and target
    X = df.iloc[:, :-1].values  # All columns except last
    Y = df.iloc[:, -1].values  # Only last column

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)

    # Initialize and Train Decision Tree Classifier
    dt_clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=5, min_samples_leaf=5)
    dt_clf_gini.fit(X_train, y_train)

    # Get the model score
    y_pred = dt_clf_gini.predict(X_test)
    score = dt_clf_gini.score(X_test, y_test)
    confusion_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    classification_report = sklearn.metrics.classification_report(y_test, y_pred)

    return dt_clf_gini, X_test, y_test, score, confusion_matrix, classification_report

def test_model(model, X_test, y_test):
    # Get the model score
    y_pred = model.predict(X_test)
    score = model.score(X_test, y_test)
    confusion_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    classification_report = sklearn.metrics.classification_report(y_test, y_pred)

    print(f"Model score: {score}")
    print(f"Confusion matrix: {confusion_matrix}")
    print(f"Classification report: {classification_report}")

    return score, confusion_matrix, classification_report

def predict(model, X_test):
    return model.predict(X_test)

def save_model(model, path):

    # Save Model Using Pickle
    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)

    return model

def load_model(path):
    with open(path, "rb") as model_file:
        model = pickle.load(model_file)
    return model


def main():
    df = load_data("data/adult.csv")
    print(f"Data after loading: {df.head()}")
    df = preprocess_data(df)
    model, X_test, y_test, score, confusion_matrix, classification_report = train_model(df)
    print(f"Model score: {score}")
    print(f"Confusion matrix: {confusion_matrix}")
    print(f"Classification report: {classification_report}")
    test_model(model, X_test, y_test)
    save_model(model, "models/model.pkl")
    return model

if __name__ == "__main__":
    main()