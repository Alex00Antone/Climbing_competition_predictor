import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import pickle

from modeling import predict 

app = Flask(__name__)


MODEL_PATH = "data/model1.pkl1"

try:
    with open(MODEL_PATH, "rb") as f:

        model_data = pickle.load(f)
    print("Model data loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")

    model_data = None


def ValuePredictor(form_dict):
    """
    Takes a dict from request.form and transforms it into the format
    required by the trained model (numeric types, correct features).
    """
    if model_data is None:
        return 0 
        
    df = pd.DataFrame([form_dict])
    

    for col in ['discipline_boulder', 'discipline_lead']:
        df[col] = df[col].astype(str).str.lower().map({'yes': 1, 'no': 0}).fillna(0).astype(int)
    

    df['gender'] = df['gender'].astype(str).str.lower().str.capitalize() 
    gender_dummies = pd.get_dummies(df['gender'], prefix='gender')
    df = pd.concat([df, gender_dummies], axis=1)
    

    df['age_at_comp'] = pd.to_numeric(df['age_at_comp'], errors='coerce')

    df['adult'] = np.where(df['age_at_comp'] >= 19, 1, 0).astype(int)
    

    for col in ['year', 'month', 'dayofyear']:
 
        if col not in df.columns:

            df[col] = 0
    for col in ['season', 'athlete_id', 'event_id', 'd_cat']:
        
        df[col] = pd.to_numeric(df.get(col, 0), errors='coerce').fillna(0).astype(int)

    df['country_encoded'] = 0 
    

    df.drop(columns=['country', 'gender'], inplace=True, errors='ignore')

    for col in ['gender_male', 'gender_female']:
        if col in df.columns:
            df[col] = df[col].astype(int)
        else:
            df[col] = 0 

    


    pred = predict(model_data, df)

   
    return int(pred[0])

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    
    form_dict = request.form.to_dict()

    try:
        result = ValuePredictor(form_dict)
    except Exception as e:
        print(f"Prediction Error: {e}")

        return render_template("result.html", prediction=f"Prediction Failed (Error: {e})")

    
    label_map = {
        0: "Did Not Advance (Rank > 24)",
        1: "Qualified for Semifinals (Ranks 9–24)",
        2: "Qualified for Finals (Ranks 4–8)",
        3: "Podium (Top 3)"
    }

    prediction = label_map.get(result, f"Unknown class: {result}")

    return render_template("result.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)