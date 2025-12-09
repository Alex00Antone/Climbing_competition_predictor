import pandas as pd
import sklearn as sklearn
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def load_data(path):
    print(f"Loading data from {path}")
    df = pd.read_csv(path)
    print(df.head())
    return df

def preprocess_data(df, inplace):
    if not inplace:
        df = df.copy()


    for c in ['height', 'arm_span']:
        if c in df.columns:
            df.drop(columns=[c], inplace=True, errors='ignore')


    for c in ['firstname', 'lastname']:
        if c in df.columns:
            df.drop(columns=[c], inplace=True, errors='ignore')

    if 'paraclimbing_sport_class' in df.columns:
        df.drop(columns=['paraclimbing_sport_class'], inplace=True, errors='ignore')

    if 'birthday' in df.columns:
        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')


    if 'age_at_comp' not in df.columns:
        if 'date' in df.columns and 'birthday' in df.columns:
            df['age_at_comp'] = (df['date'] - df['birthday']).dt.days / 365.25
        elif 'age' in df.columns:

            df['age_at_comp'] = df['age']
        else:
            df['age_at_comp'] = np.nan


    if 'age' in df.columns:
        df.drop(columns=['age'], inplace=True, errors='ignore')


    if 'discipline' in df.columns:
        dummies = pd.get_dummies(df['discipline'], prefix='discipline')

        df = pd.concat([df, dummies], axis=1)

        for col in ['discipline_combined', 'discipline_speed', 'discipline_boulder&lead']:
            if col in df.columns:
                df.drop(columns=[col], inplace=True, errors='ignore')
    else:

        df['discipline_boulder'] = df.get('discipline_boulder', False)
        df['discipline_lead'] = df.get('discipline_lead', False)


    if 'gender' in df.columns:
        gender_dummies = pd.get_dummies(df['gender'], prefix='gender')
        df = pd.concat([df, gender_dummies], axis=1)
    else:
        df['gender_male'] = df.get('gender_male', False)
        df['gender_female'] = df.get('gender_female', False)

    for col in df.columns:
        if col.startswith('discipline_') and col not in ('discipline_boulder', 'discipline_lead'):

            try:
                df = df[~df[col].astype(bool)]
            except Exception:

                pass

            df.drop(columns=[col], inplace=True, errors='ignore')


    if 'event_location' in df.columns:
        df = df[~df['event_location'].astype(str).str.contains('paraclimbing', case=False, na=False)]
        df = df[~df['event_location'].astype(str).str.contains(r'\bpc\b', case=False, na=False)]


    if 'event_location' in df.columns:
        df.drop(columns=['event_location'], inplace=True, errors='ignore')


    if 'rank' in df.columns:
        df = df[df['rank'] > 0]
        df = df[df['rank'] <= 200]

   
        df['date'] = pd.NaT


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['dayofyear'] = df['date'].dt.dayofyear

   
    df = df[ (df['age_at_comp'].isna()) | (df['age_at_comp'] > 10) ]

   
    median_age = df['age_at_comp'].median()

    fill_center = (median_age if not np.isnan(median_age) else 25.0) + 5
    missing_mask = df['age_at_comp'].isna()
    if missing_mask.any():
        df.loc[missing_mask, 'age_at_comp'] = fill_center + np.random.normal(0, 5, size=missing_mask.sum())


    df['adult'] = np.where(df['age_at_comp'] >= 19, True, False)


    if 'country' in df.columns:
        country_counts = df['country'].value_counts()
        df['country_encoded'] = df['country'].map(country_counts).fillna(0).astype(int)
        df.drop(columns=['country'], inplace=True, errors='ignore')
    elif 'country_encoded' not in df.columns:
        df['country_encoded'] = 0


    if 'round_result' not in df.columns:
        if 'rank' in df.columns:
            def map_round(rank):
                if rank <= 3:
                    return 3
                elif rank <= 8:
                    return 2
                elif rank <= 24:
                    return 1
                else:
                    return 0
            df['round_result'] = df['rank'].apply(map_round)
            df.drop(columns=['rank'], inplace=True, errors='ignore')
        else:
            raise ValueError("Input DataFrame must contain 'rank' or 'round_result' for target creation.")

    
    if 'birthday' in df.columns:
        df.drop(columns=['birthday'], inplace=True, errors='ignore')

    
    for col in ['discipline_boulder', 'discipline_lead', 'gender_male', 'gender_female']:
        if col not in df.columns:
            df[col] = False

    
    print("Preprocessing complete. Columns:", df.columns.tolist())
    return df

def train_model(df):

    X = df.drop(columns=['date', 'round_result'], errors='ignore') if 'date' in df.columns else df.drop(columns=['round_result'])
    y = df['round_result']

    for col in ['year', 'month', 'dayofyear']:
        if col not in X.columns:
            X[col] = 0


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()

    scaler = StandardScaler()
    X_train_num = scaler.fit_transform(X_train[numeric_cols])
    X_test_num = scaler.transform(X_test[numeric_cols])

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[numeric_cols] = X_train_num
    X_test_scaled[numeric_cols] = X_test_num

    sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

    
    model = XGBClassifier(
        n_estimators=1000,
        reg_alpha=1.0,
        reg_lambda=2.0,
        min_child_weight=5,
        max_depth=6,
        subsample=0.7,
        colsample_bytree=0.7,
        learning_rate=0.03,
        gamma=1,
        tree_method='hist',
        eval_metric='mlogloss',
        objective='multi:softprob',
        num_class=4,
        early_stopping_rounds=30,
        n_jobs=-1,
        random_state=RANDOM_STATE,
        use_label_encoder=False
    )


    eval_set = [(X_test_scaled, y_test)]
    model.fit(
        X_train_scaled,
        y_train,
        sample_weight=sample_weights,
        eval_set=eval_set,
        verbose=False
    )


    y_pred = model.predict(X_test_scaled)
    score = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = sk_classification_report(y_test, y_pred)

    model_data = {
        'model': model,
        'scaler': scaler,
        'numeric_cols': numeric_cols,
        'feature_columns': X_train_scaled.columns.tolist()
    }


    return model_data, X_test_scaled, y_test, score, cm, cr

def test_model(model_data, X_test, y_test):
    """
    Evaluate a loaded/trained model_data (dict returning from train_model).
    Prints and returns score, confusion matrix, classification report.
    """
    model = model_data['model']
    y_pred = model.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = sk_classification_report(y_test, y_pred)

    print(f"Model score: {score}")
    print(f"Confusion matrix:\n{cm}")
    print(f"Classification report:\n{cr}")

    return score, cm, cr


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

def save_model(model, path):


    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)

    return model

def load_model(path):
    with open(path, "rb") as model_file:
        model = pickle.load(model_file)
    return model


def main():
    df = load_data("output.csv")

    model_data, X_test, y_test, score, cm, cr = train_model(df)

    print("Training complete.")
    print(f"Accuracy: {score}")
    print("Confusion matrix:")
    print(cm)
    print("Classification report:")
    print(cr)

    
    save_model(model_data, "models/weighted_xgb_model.pkl")

    
    test_model(model_data, X_test, y_test)

    return model_data


if __name__ == "__main__":
    main()