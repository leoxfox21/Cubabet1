import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

FILE = "data/dataset.csv"
MODEL_FILE = "data/model.json"


def train():

    df = pd.read_csv(FILE)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scale_pos_weight = len(y_train[y_train==0]) / len(y_train[y_train==1])

    model = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        scale_pos_weight=scale_pos_weight
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    accuracy = model.score(X_test, y_test)

    print("Accuracy:", accuracy)

    model.save_model(MODEL_FILE)