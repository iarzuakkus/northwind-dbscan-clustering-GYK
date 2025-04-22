from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Literal
from model import apply_dbscan
from database_connect import cutomer_segmentation, product_segmentation, supplier_segmentation, country_segmentation
from visualize import plot_dynamic_segmentation
import numpy as np

app = FastAPI(
    title="Northwind DBSCAN Segmentasyon API",
    version="1.0.0"
)

# Swagger'da dropdown olarak gözükecek segmentler
SegmentType = Literal["customers", "products", "suppliers", "countries"]

# Segmentlere karşılık gelen veri çekme fonksiyonları (veritabanından)
segment_sources = {
    "customers": cutomer_segmentation,
    "products": product_segmentation,
    "suppliers": supplier_segmentation,
    "countries": country_segmentation
}

@app.get("/cluster")
def get_clusters(segment: SegmentType = Query(..., description="Segment seçimi")):
    df = segment_sources[segment]()          # Veriyi çek
    clustered_df = apply_dbscan(df)          # DBSCAN uygula
    clustered_df = clustered_df.replace({np.nan: None})  # NaN'leri JSON'a uygun hale getir
    return clustered_df.to_dict(orient="records")


@app.get("/outliers")
def get_outliers(segment: SegmentType = Query(..., description="Segment seçimi")):
    df = segment_sources[segment]()              # Veriyi veritabanından çek
    clustered_df = apply_dbscan(df)              # Tüm veriye cluster uygula
    outliers = clustered_df[clustered_df["cluster"] == -1]  # Aykırıları filtrele
    outliers = outliers.replace({np.nan: None})  # JSON için temizle
    return outliers.to_dict(orient="records")

@app.get("/columns")
def get_available_columns(segment: SegmentType = Query(..., description="Segment seçimi")):
    df = segment_sources[segment]()
    clustered_df = apply_dbscan(df)
    numeric_cols = clustered_df.select_dtypes(include=["number"]).columns.tolist()
    feature_cols = [col for col in numeric_cols if col != "cluster"]
    return {"columns": feature_cols}

@app.get("/plot")
def plot_segment(
    segment: SegmentType = Query(...),
    x_col: str = Query(...),
    y_col: str = Query(...)
):
    df = segment_sources[segment]()
    clustered_df = apply_dbscan(df)

    if x_col not in clustered_df.columns or y_col not in clustered_df.columns:
        return JSONResponse(status_code=400, content={"error": "Geçersiz sütun adı"})

    plot_dynamic_segmentation(clustered_df, x_col, y_col, title=f"{segment.title()} Segmentasyonu")
    return {"status": "Grafik çizildi"}


#python -m uvicorn main:app --reload
#http://127.0.0.1:8000/docs