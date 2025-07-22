import numpy as np
from src.utils.pattern_learner import PatternLearner

def test_anomaly_detection_length():
    data = np.vstack([
        np.zeros((10, 2)),
        np.ones((5, 2)) * 5,
        np.random.uniform(10, 15, (2, 2))
    ])
    learner = PatternLearner(eps=0.5, min_samples=3)
    learner.fit(data)
    labels = learner.detect_anomalies(data)
    assert labels.shape[0] == data.shape[0]
