import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from load_data import load_shopper_data

def train_sklearn_model():
    print("Training Sklearn Model")
    X_train, X_test, y_train, y_test, scaler, feature_names = load_shopper_data()

    print("Loading RandomForestClassifier")
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )

    print("Fitting model")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print("Sklearn Model Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    print("Saving model")
    with open("models/sklearn_model.pkl", "wb") as f:
        pickle.dump({
            "model": model,
            "scaler": scaler,
            "feature_names": feature_names
        }, f)

    print("Saved sklearn_model.pkl to models/sklearn_model.pkl")

if __name__ == "__main__":
    train_sklearn_model()
