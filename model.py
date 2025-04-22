import pandas as pd
import numpy as np
import psycopg2
from database_connect import cutomer_segmentation, product_segmentation, supplier_segmentation, country_segmentation
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

scaler = StandardScaler()

def find_optimal_eps(X_scaled, min_samples=3):
    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances,_ = neighbors.kneighbors(X_scaled)

    distances = np.sort(distances[:, min_samples-1])
    kneedle = KneeLocator(range(len(distances)), distances, curve='convex', direction='increasing')
    optimal_eps = distances[kneedle.elbow]
    return optimal_eps

#PROBLEM-1-2-3-4
def apply_dbscan(df):
    X = df.iloc[:, 1:]
    X_scaled = scaler.fit_transform(X)
    optimal_eps = find_optimal_eps(X_scaled)
    dbscan = DBSCAN(eps = optimal_eps, min_samples=3)

    df['cluster'] = dbscan.fit_predict(X_scaled)
    
    #outliers = df[df['cluster'] == -1]
    return df

if __name__ ==  '__main__':
    
    data_frames = [cutomer_segmentation(),product_segmentation(),
                   supplier_segmentation(),country_segmentation()]

    segment_names = [
    "Müşteri Segmentasyonu", "Ürün Segmentasyonu",
    "Tedarikçi Segmentasyonu", "Ülke Segmentasyonu"
    ]

    for name, df in zip(segment_names, data_frames):
        outliers = apply_dbscan(df)
        outliers = outliers[outliers['cluster'] == -1]
        print(f"\n {name} - Aykırı veri sayısı: {len(outliers)}")
        print(outliers.iloc[:, 1:])
