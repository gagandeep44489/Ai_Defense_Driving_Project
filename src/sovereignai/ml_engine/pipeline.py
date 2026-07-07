"""Complete baseline machine-learning pipeline for cyber telemetry."""
from dataclasses import dataclass
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

@dataclass(frozen=True)
class TrainingResult:
    """Metrics and trained pipeline returned by training."""
    accuracy: float
    f1: float
    pipeline: Pipeline

class ModelFactory:
    """Factory for baseline model families including optional boosted models."""
    def create(self, name: str) -> object:
        """Create a model by strategy name."""
        if name == 'isolation_forest': return IsolationForest(random_state=42, contamination='auto')
        if name == 'random_forest': return RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        if name == 'xgboost':
            from xgboost import XGBClassifier
            return XGBClassifier(eval_metric='logloss', random_state=42)
        if name == 'lightgbm':
            from lightgbm import LGBMClassifier
            return LGBMClassifier(random_state=42)
        if name == 'catboost':
            from catboost import CatBoostClassifier
            return CatBoostClassifier(verbose=False, random_seed=42)
        raise ValueError(f'unsupported model: {name}')

class TrainingPipeline:
    """Validates data, engineers numeric features, trains, and evaluates models."""
    def train(self, frame: pd.DataFrame, target: str = 'label', model_name: str = 'random_forest') -> TrainingResult:
        """Train a model on a dataframe and return metrics."""
        if target not in frame.columns: raise ValueError(f'missing target column {target}')
        clean = frame.dropna().copy(); x = clean.drop(columns=[target]).select_dtypes(include='number'); y = clean[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42, stratify=y if y.nunique()>1 else None)
        pipe = Pipeline([('scale', StandardScaler()), ('model', ModelFactory().create(model_name))])
        pipe.fit(x_train, y_train); pred = pipe.predict(x_test)
        return TrainingResult(float(accuracy_score(y_test, pred)), float(f1_score(y_test, pred, average='weighted')), pipe)
