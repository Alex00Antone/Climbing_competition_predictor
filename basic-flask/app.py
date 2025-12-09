import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import pickle
from modeling import predict   

app = Flask(__name__)


MODEL_PATH = "data/model.pkl"

with open(MODEL_PATH, "rb") as f:
    model_data = pickle.load(f)


def ValuePredictor(form_dict):
    """
    Takes a dict from request.form and returns model prediction.
    """
    
    df = pd.DataFrame([form_dict])
    
   
    for col in ['discipline_boulder', 'discipline_lead']:
        df[col] = df[col].astype(str).str.lower().map({'yes': True, 'no': False})
    
    
    df['gender'] = df['gender'].astype(str).str.lower().str.capitalize() 
    gender_dummies = pd.get_dummies(df['gender'], prefix='gender')
    df = pd.concat([df, gender_dummies], axis=1)
    
  
    df['age_at_comp'] = pd.to_numeric(df['age_at_comp'], errors='coerce')
    df['adult'] = np.where(df['age_at_comp'] >= 19, True, False)
    
   
    df.drop(columns=['country', 'gender'], inplace=True, errors='ignore')

   
    for col in ['discipline_boulder', 'discipline_lead', 'gender_male', 'gender_female', 'adult']:
        if col in df.columns:
            df[col] = df[col].astype(bool) 
    
    
    pred = predict(model_data, df)

   
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    
    form_dict = request.form.to_dict()

    result = ValuePredictor(form_dict)

    
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