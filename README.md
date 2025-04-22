# Northwind DBSCAN Segmentasyon API

Bu proje, Northwind veritabanındaki verileri kullanarak DBSCAN algoritması ile segmentasyon (kümeleme) yapar. Hedef, ürünler, müşteriler, tedarikçiler ve ülkeler üzerinden alışılmadık davranışları, aykırı değerleri ve kümeleri tespit etmektir.

## Teknolojiler
- FastAPI 
- Scikit-learn
- Pandas
- SQLAlchemy & psycopg2
- Matplotlib
- Northwind veritabanı (PostgreSQL)

---

##  Proje Yapısı

```
.
├── main.py                 # FastAPI uygulama tanımı ve endpointler
├── model.py                # DBSCAN uygulayan fonksiyonlar
├── visualize.py            # Matplotlib ile grafik çizimi
├── database_connect.py     # Segment verilerini çeken SQL sorguları
└── README.md
```

---

## Endpointler

### `/cluster`
Seçilen segmenti DBSCAN algoritması ile kümeleyerek tüm veriyi cluster etiketiyle döner.

### `/outliers`
Seçilen segmentte `cluster == -1` olan aykırı gözlemleri döner.

### `/columns`
Seçilen segmentteki sayısal sütunları döner. x/y ekseni için kullanılabilir.

### `/plot`
Segment, x_col, y_col girilerek grafik çizer. Swagger'da JSON döner ama grafik local ortamda matplotlib ile görüntülenir.

---

## 📊 Örnek Segmentler ve Özellikler

### ● Müşteri Segmentasyonu
- total_orders
- total_spent
- avg_order_value

### ● Ürün Segmentasyonu
- avg_unit_price
- sales_frequency
- avg_quantity
- unique_customer_count

### ● Tedarikçi Segmentasyonu
- num_of_products_supplied
- total_spent
- avg_spent
- num_of_customer

### ● Ülke Segmentasyonu
- total_order_count
- avg_spent
- avg_items_per_order

---

## ⚡þ Başlatma
```bash
python -m uvicorn main:app --reload
```
Uygulama çalıştıktan sonra Swagger arayüzü:
> http://127.0.0.1:8000/docs

---

**Hazırlayan:** [iarzuakkus](https://github.com/iarzuakkus)  

