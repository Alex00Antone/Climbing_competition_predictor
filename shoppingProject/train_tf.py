import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.metrics import accuracy_score, classification_report
from load_data import load_shopper_data

def train_tf_model():
    print("Training TensorFlow Model")
    X_train, X_test, y_train, y_test, scaler, feature_names = load_shopper_data()

    print("Building model")
    model = Sequential([
        Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid")
    ])

    print("Compiling model")
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    print("Fitting model")
    model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=10,
        batch_size=32,
        verbose=1
    )

    print("Predicting model")
    preds = model.predict(X_test)
    preds = (preds > 0.5).astype(int).flatten()

    print("TF Model Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    model.save("models/tf_model.keras")
    print("Saved tf_model.keras")

if __name__ == "__main__":
    train_tf_model()
