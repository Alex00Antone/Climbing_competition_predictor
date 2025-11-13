from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

# ------------------------------------------------
# Load Sklearn Model
# ------------------------------------------------
with open("models/sklearn_model.pkl", "rb") as f:
    skl_bundle = pickle.load(f)

skl_model = skl_bundle["model"]
skl_scaler = skl_bundle["scaler"]
skl_features = skl_bundle["feature_names"]

# ------------------------------------------------
# Load TensorFlow Model
# ------------------------------------------------
tf_model = tf.keras.models.load_model("models/tf_model.keras")


# ------------------------------------------------
# Home Page
# ------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------------------------
# Sklearn Page + Prediction
# ------------------------------------------------
@app.route("/sklearn", methods=["GET", "POST"])
def sklearn_page():
    prediction = None

    if request.method == "POST":
        data = {key: request.form.get(key) for key in request.form}

        # Convert types
        for key in data:
            if data[key].lower() in ["true", "false"]:
                data[key] = data[key].lower() == "true"
            else:
                try:
                    data[key] = float(data[key])
                except:
                    pass

        # Convert to DataFrame and one-hot encode
        df = pd.DataFrame([data])
        df = pd.get_dummies(df)
        df = df.reindex(columns=skl_features, fill_value=0)

        X = skl_scaler.transform(df)
        pred = skl_model.predict(X)[0]

        prediction = "Revenue Likely" if pred == 1 else "Revenue Unlikely"

    return render_template("sklearn.html", prediction=prediction)


# ------------------------------------------------
# TensorFlow Page + Prediction
# ------------------------------------------------
@app.route("/tensorflow", methods=["GET", "POST"])
def tensorflow_page():
    prediction = None
    probability = None

    if request.method == "POST":
        data = {key: request.form.get(key) for key in request.form}

        # Convert types
        for key in data:
            if data[key].lower() in ["true", "false"]:
                data[key] = data[key].lower() == "true"
            else:
                try:
                    data[key] = float(data[key])
                except:
                    pass

        # Convert to DataFrame
        df = pd.DataFrame([data])
        df = pd.get_dummies(df)
        df = df.reindex(columns=skl_features, fill_value=0)

        X = skl_scaler.transform(df)
        pred_prob = tf_model.predict(X)[0][0]
        pred_label = int(pred_prob > 0.5)

        prediction = "Revenue Likely" if pred_label == 1 else "Revenue Unlikely"
        probability = round(pred_prob * 100, 2)

    return render_template("tensorflow.html", prediction=prediction, probability=probability)


if __name__ == "__main__":
    app.run(debug=True)
