from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

def print_clustering_metrics(kmeans, transform_result):
    print('SSE %s' % kmeans.inertia_)
    print('Silhouette %s' % silhouette_score(transform_result, kmeans.labels_))
    print('Separation %s' % davies_bouldin_score(transform_result, kmeans.labels_))