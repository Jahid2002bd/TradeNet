import numpy as np
import pytest
from src.utils.pattern_visualizer import plot_clusters

def test_insufficient_features_raises():
    with pytest.raises(ValueError):
        plot_clusters(np.ones((5, 1)), np.zeros(5))
