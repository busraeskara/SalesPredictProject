# SalesPredictProject

Bu proje, Bu proje, **Northwind veritabanındaki** sipariş verilerini kullanarak ürün bazlı satış tahmini yapan bir makine öğrenmesi modelini REST API aracılığıyla erişilebilir hale getirmektedir. Dış sistemler bu API'yi kullanarak belirli ürünlere ait satış tahminleri alabilir. Python, FastAPI, PostgreSQL, scikit-learn gibi modern araçlar kullanılarak geliştirilmiştir. API, gelecekteki ürün taleplerini tahmin ederek işletmelerin daha iyi kararlar almasını hedefler.

---

## Özellikler

- Ürün geçmiş verilerine göre satış tahmini yapar  
- RESTful API mimarisi  
- PostgreSQL veritabanı kullanımı  
- Model eğitimi ve tahmin işlemleri  
- Swagger UI üzerinden API dokümantasyonu  

---

## Kullanılan Teknolojiler

- Python  
- FastAPI  
- scikit-learn  
- SQLAlchemy  
- PostgreSQL
- Pydantic
- Pandas, NumPy
- DecisionTreeRegressor
- Swagger UI / Postman (API dokümantasyonu)

---

## Proje Yapısı

<h3>main.py<h3>– API ve Model Entegrasyon Katmanı
Bu dosya, projenin ana uygulama dosyasıdır ve aşağıdaki temel işlevleri yerine getirir:

🚀 FastAPI Sunucusunu Başlatır
FastAPI framework'ü ile RESTful API endpoint'lerini tanımlar.

API dökümantasyonu için Swagger UI desteklidir (/docs altında otomatik olarak erişilebilir).

🧠 Makine Öğrenmesi Modeli
Northwind verilerinden ürün bazlı geçmiş sipariş verilerini kullanarak satış tahmin modeli (Decision Tree Regressor) eğitir.

Eğitim, @app.post("/train_model") endpoint’i ile tetiklenebilir.

Eğitim verisi için:

Sipariş, sipariş detayları ve ürünler tabloları birleştirilir.

Zaman, ay, haftanın günü gibi yeni özellikler çıkarılır.

Veriler StandardScaler ile ölçeklenir.

Eğitilen model .pkl formatında diske kaydedilir ve @app.post("/predict") endpoint'i ile tahmin yapılabilir.

📦 API Endpoint’leri
Aşağıdaki kaynaklar için GET endpoint'leri sağlar:

/orders: Siparişleri listeler.

/order_details: Sipariş detaylarını listeler.

/products: Ürünleri listeler.

/customers: Müşterileri listeler.

/categories: Ürün kategorilerini listeler.

📊 Tahmin ve Özet Endpoint’leri
/predict: Ürün ve tarih bilgisine göre satış tahmini döner.

/monthly_sales_summary: Aylık toplam satış ve gelir verilerini döner.

/product_sales_summary: Ürün bazlı satış ve gelir özetlerini verir.

🧱 Özellik Mühendisliği
Zaman serisi temelli değişkenler oluşturulur: ay, haftanın günü, hafta sonu vb.

Ürün fiyatları için kategorik değişken (low, medium, high) oluşturulur.

Müşteri segmentasyonu yapılır: her müşterinin en çok alışveriş yaptığı ürün kategorisi belirlenir (favorite_category).

🔐 Hata Yönetimi ve Loglama
Her endpoint için hata yönetimi yapılır.

Uygulama içi hatalar logging modülü ile loglanır.


## ⚙️ Kurulum ve Çalıştırma

### 1. Reposu Klonla


git clone https://github.com/busraeskara/SalesPredictProject.git
cd SalesPredictProject
