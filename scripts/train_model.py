"""Train a baseline model using synthetic network logs."""
from pathlib import Path
import pandas as pd
from sovereignai.ml_engine.pipeline import TrainingPipeline

if __name__ == '__main__':
    df = pd.read_csv(Path('data/samples/network_logs.csv'))
    result = TrainingPipeline().train(df.drop(columns=['source_ip','destination_ip','protocol']), target='label')
    print({'accuracy': result.accuracy, 'f1': result.f1})
