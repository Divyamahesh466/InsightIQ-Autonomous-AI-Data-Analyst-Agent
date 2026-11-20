
import pandas as pd
import numpy as np
import inspect

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import (
    ExtraTreesClassifier,
    ExtraTreesRegressor
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def train_model(df, target, task_type="Auto", test_size=0.2):

    # 1. Validate dataset
    if target not in df.columns:
        raise ValueError("Selected target column does not exist.")

    if not 0.1 <= test_size <= 0.4:
        raise ValueError("Test size must be between 0.1 and 0.4.")

    work = df.copy()

    # Remove infinite values
    work = work.replace([np.inf, -np.inf], np.nan)

    # Remove rows with missing target
    work = work.dropna(subset=[target])

    if len(work) < 10:
        raise ValueError("At least 10 valid rows are required.")

    y = work[target]
    X = work.drop(columns=[target])

    if X.empty:
        raise ValueError("At least one feature column is required.")

    if y.nunique() < 2:
        raise ValueError("Target must contain at least two different values.")

    # 2. Detect task type
    if task_type == "Auto":
        is_classification = (
            not pd.api.types.is_numeric_dtype(y)
            or y.nunique() <= 15
        )
    else:
        is_classification = task_type == "Classification"

    if is_classification and y.nunique() < 2:
        raise ValueError("Classification requires two or more classes.")

    # 3. Convert date columns into numeric features
    date_cols = X.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    for col in date_cols:
        X[col + "_year"] = X[col].dt.year
        X[col + "_month"] = X[col].dt.month
        X[col + "_day"] = X[col].dt.day
        X[col + "_weekday"] = X[col].dt.dayofweek

    X = X.drop(columns=date_cols)

    # 4. Remove ID-like and constant columns
    remove_cols = []

    for col in X.columns:
        unique_count = X[col].nunique(dropna=True)
        unique_ratio = unique_count / max(len(X), 1)

        col_name = str(col).lower().replace(" ", "_")

        if unique_count <= 1:
            remove_cols.append(col)

        elif (
            "id" in col_name
            or col_name in ["row_number", "order_number"]
        ) and unique_ratio > 0.5:
            remove_cols.append(col)

        elif unique_ratio > 0.98 and not pd.api.types.is_numeric_dtype(X[col]):
            remove_cols.append(col)

    X = X.drop(columns=remove_cols, errors="ignore")

    if X.empty:
        raise ValueError("No useful feature columns remain after cleaning.")

    # 5. Identify numerical and categorical features
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = X.select_dtypes(
        include=["object", "category", "bool", "string"]
    ).columns.tolist()

    transformers = []

    if numeric_cols:
        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ])

        transformers.append(
            ("num", numeric_pipeline, numeric_cols)
        )

    if categorical_cols:
        # Limit categories to reduce processing time
        encoder_args = {
            "handle_unknown": "ignore"
        }

        if "max_categories" in inspect.signature(
            OneHotEncoder
        ).parameters:
            encoder_args["max_categories"] = 30

        if "min_frequency" in inspect.signature(
            OneHotEncoder
        ).parameters:
            encoder_args["min_frequency"] = 5

        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(**encoder_args))
        ])

        transformers.append(
            ("cat", categorical_pipeline, categorical_cols)
        )

    if not transformers:
        raise ValueError("No suitable numerical or categorical features found.")

    preprocess = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    # 6. Split dataset
    stratify = None

    if is_classification:
        class_counts = y.value_counts()

        if (
            class_counts.min() >= 2
            and int(len(y) * test_size) >= y.nunique()
            and int(len(y) * (1 - test_size)) >= y.nunique()
        ):
            stratify = y

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
            stratify=stratify
        )
    except ValueError as exc:
        raise ValueError(f"Dataset splitting failed: {exc}")

    # 7. Fast model
    if is_classification:
        estimator = ExtraTreesClassifier(
            n_estimators=80,
            max_depth=15,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    else:
        estimator = ExtraTreesRegressor(
            n_estimators=80,
            max_depth=15,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

    # 8. Train model
    model = Pipeline([
        ("preprocess", preprocess),
        ("model", estimator)
    ])

    model.fit(X_train, y_train)

    # 9. Predictions
    predictions = model.predict(X_test)

    # 10. Evaluation
    if is_classification:
        metrics = {
            "Task": "Classification",
            "Accuracy": round(
                accuracy_score(y_test, predictions), 4
            ),
            "Training Rows": len(X_train),
            "Testing Rows": len(X_test),
            "Features Used": X.shape[1]
        }

    else:
        rmse = np.sqrt(
            mean_squared_error(y_test, predictions)
        )

        metrics = {
            "Task": "Regression",
            "MAE": round(
                mean_absolute_error(y_test, predictions), 4
            ),
            "RMSE": round(float(rmse), 4),
            "R2 Score": round(
                r2_score(y_test, predictions), 4
            ),
            "Training Rows": len(X_train),
            "Testing Rows": len(X_test),
            "Features Used": X.shape[1]
        }

    # 11. Actual vs Predicted
    preview = pd.DataFrame({
        "Actual": y_test.reset_index(drop=True),
        "Predicted": pd.Series(predictions)
    })

    return model, metrics, preview
