import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_shopper_data(path="data/online_shoppers_intention.csv"):
    df = pd.read_csv(path)

    # Target column
    y = df["Revenue"].astype(int)

    # Basic preprocessing: drop non-numeric or encode simple ones
    X = df.drop(columns=["Revenue"])

    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale numeric features for ML models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X_train.columns
