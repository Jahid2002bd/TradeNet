# src/utils/pattern_visualizer.py

"""
pattern_visualizer.py

Visualizes clustered patterns and anomalies detected by PatternLearner.
Requires matplotlib and numpy.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from typing import Optional, Sequence


def plot_clusters(
    features: np.ndarray,
    cluster_ids: np.ndarray,
    title: str = "Cluster Plot",
    feature_names: Optional[Sequence[str]] = None
) -> None:
    """
    Scatter‐plot first two features, coloring by cluster ID.
    Anomalies (cluster_id == -1) are highlighted in red.

    Parameters:
        features     (np.ndarray): shape (n_samples, n_features)
        cluster_ids  (np.ndarray): shape (n_samples,), cluster labels
        title          (str): plot title
        feature_names (Sequence[str], optional): names for axes
    """
    if features.ndim != 2 or features.shape[1] < 2:
        raise ValueError("Need at least two features to plot clusters.")
    x_vals = features[:, 0]
    y_vals = features[:, 1]

    # Use tab10 colormap for clusters
    palette = cm.get_cmap("tab10")
    unique_ids = np.unique(cluster_ids)

    plt.figure(figsize=(8, 6))
    for cid in unique_ids:
        mask = (cluster_ids == cid)
        xs = x_vals[mask]
        ys = y_vals[mask]

        if cid == -1:
            color = "red"
            label = "Anomaly"
        else:
            color = palette(int(cid) % 10)
            label = f"Cluster {cid}"

        plt.scatter(
            xs,
            ys,
            label=label,
            alpha=0.6,
            s=40,
            color=color
        )

    plt.title(title)
    xlabel = feature_names[0] if feature_names else "Feature 0"
    ylabel = feature_names[1] if feature_names else "Feature 1"
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()
