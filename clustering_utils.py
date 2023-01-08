from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import numpy as np
import pandas as pd

def print_clustering_metrics(kmeans, transform_result):
    print('SSE %s' % kmeans.inertia_)
    print('Silhouette %s' % silhouette_score(transform_result, kmeans.labels_))
    print('Separation %s' % davies_bouldin_score(transform_result, kmeans.labels_))

def get_clustering_metrics(kmeans, transform_result):
    textstr = '\n'.join((
        r'$SSE=%f$' % (kmeans.inertia_, ),
        r'$Silhouette=%f$' % (silhouette_score(transform_result, kmeans.labels_), ),
        r'$Separation=%f$' % (davies_bouldin_score(transform_result, kmeans.labels_), )))
    return textstr

def apply_correlation_threshold(df: pd.DataFrame, correlation_method: str, threshold: float) -> pd.DataFrame:
    # Create correlation matrix
    corr_matrix = df.corr(numeric_only=True, method=correlation_method).abs()

    # Select upper triangle of correlation matrix (correlation matrix is symmetrical)
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Find features with correlation greater than the threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]

    # Drop features 
    return df.drop(to_drop, axis=1)