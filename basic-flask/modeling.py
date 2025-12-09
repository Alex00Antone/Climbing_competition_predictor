import pandas as pd
import numpy as np
import pickle


def load_model(path):
    with open(path, "rb") as model_file:
        model_data = pickle.load(model_file)
    return model_data


def predict(model_data, X):
    
    model = model_data['model']
    scaler = model_data['scaler']
    numeric_cols = model_data['numeric_cols']
    feature_columns = model_data['feature_columns']


    if isinstance(X, dict):
        X = pd.DataFrame([X])
    elif isinstance(X, list):
        X = pd.DataFrame(X)

    for col in feature_columns:
        if col not in X.columns:
           
            X[col] = 0


    X = X[feature_columns]

 
    if numeric_cols:

        X[numeric_cols] = scaler.transform(X[numeric_cols])


    preds = model.predict(X)
    return np.array(preds)

