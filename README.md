# SalesPredictProject

Bu proje, **Northwind veritabanındaki** sipariş verilerini kullanarak ürün bazlı satış tahmini yapan bir makine öğrenmesi modelini REST API aracılığıyla erişilebilir hale getirmektedir. Dış sistemler bu API'yi kullanarak belirli ürünlere ait satış tahminleri alabilir. Python, FastAPI, PostgreSQL, scikit-learn gibi modern araçlar kullanılarak geliştirilmiştir. API, gelecekteki ürün taleplerini tahmin ederek işletmelerin daha iyi kararlar almasını hedefler.

---

## Özellikler

- Ürün geçmiş verilerine göre satış tahmini yapar.
- RESTful API mimarisi ile erişilebilir.
- PostgreSQL veritabanı kullanımı.  
- Model eğitimi ve tahmin işlemleri  
- Swagger UI üzerinden API dokümantasyonu sağlar.

---

## Kullanılan Teknolojiler

- Python  
- FastAPI  
- scikit-learn  
- SQLAlchemy  
- PostgreSQL
- Pydantic
- Pandas, NumPy, Joblib
- Uvicorn
- DecisionTreeRegressor
- Swagger UI / Postman (API dokümantasyonu)

---

## Proje Yapısı

### *main.py* – API ve Model Entegrasyon Katmanı
Bu dosya, projenin ana uygulama dosyasıdır ve aşağıdaki temel işlevleri yerine getirir:

#### FastAPI Sunucusunu Başlatır
- FastAPI framework'ü ile RESTful API endpoint'lerini tanımlar.
- API dökümantasyonu için Swagger UI desteklidir (/docs altında otomatik olarak erişilebilir).
- Swagger UI / Postman (API dokümantasyonu).

#### Makine Öğrenmesi Modeli
- Northwind verilerinden ürün bazlı geçmiş sipariş verilerini kullanarak satış tahmin modeli (Decision Tree Regressor) eğitir.
- Eğitim, @app.post("/train_model") endpoint’i ile tetiklenebilir.
- Eğitim verisi için:
  - Sipariş, sipariş detayları ve ürünler tabloları birleştirilir.
  - Zaman, ay, haftanın günü gibi yeni özellikler çıkarılır.
  - Veriler *StandardScaler* ile ölçeklenir.
- Eğitilen model decision_tree_model.pkl formatında diske kaydedilir ve @app.post("/predict") endpoint'i ile tahmin yapılabilir.
- Modelin performansı MAE, MSE, RMSE, R² metrikleri ile değerlendirilir.

#### API Endpoint’leri

Aşağıdaki kaynaklar için GET endpoint'leri sağlar:
  - /orders: Siparişleri listeler.
  - /order_details: Sipariş detaylarını listeler.
  - /products: Ürünleri listeler.
  - /customers: Müşterileri listeler.
  - /categories: Ürün kategorilerini listeler.
    
#### Tahmin ve Özet Endpoint’leri
- /predict: Ürün ve tarih bilgisine göre satış tahmini döner.
- /monthly_sales_summary: Aylık toplam satış ve gelir verilerini döner.
- /product_sales_summary: Ürün bazlı satış ve gelir özetlerini verir.

#### Özellik Mühendisiliği
- Zaman serisi temelli değişkenler oluşturulur: ay, haftanın günü, hafta sonu vb.
- Ürün fiyatları için kategorik değişken (low, medium, high) oluşturulur.
- Müşteri segmentasyonu yapılır: her müşterinin en çok alışveriş yaptığı ürün kategorisi belirlenir (favorite_category).

#### Hata Yönetimi ve Loglama
- Her endpoint için hata yönetimi yapılır.
- Uygulama içi hatalar logging modülü ile loglanır.

### *database.py* 
Bu dosya, veritabanı bağlantısını yönetmek ve veritabanından veri çekmek için kullanılan yardımcı fonksiyonları içerir. Projede SQLAlchemy kullanılarak Northwind veritabanına bağlantı sağlanır.

#### Temel Bileşenler:
- engine: config.py dosyasındaki DATABASE_URL üzerinden SQLAlchemy motoru oluşturulur. Bu motor, PostgreSQL veritabanına bağlanmak için kullanılır.
- SessionLocal: SQLAlchemy oturumlarını yönetmek için sessionmaker ile oluşturulan yapı.
- Base: SQLAlchemy ORM modelleri için temel sınıf olarak kullanılır.
- fetch_table(table_name): Veritabanındaki istenen tabloyu Pandas DataFrame olarak döndürür. Böylece veri işleme ve analiz işlemleri kolayca yapılabilir.
  
#### Kullanım Amacı:
- Veritabanına bağlanmak.
- API ve model eğitimi için gerekli tabloları veri çerçevesi (DataFrame) olarak almak.
- Uygulamanın veritabanı ile olan bağlantı katmanını soyutlayarak daha okunabilir ve yönetilebilir hale getirmek.

### *config.py* 
Bu dosya, veritabanı bağlantı bilgilerini yükler ve ortam değişkenlerinden alır. .env dosyasını kullanarak gizli bilgileri (veritabanı kullanıcı adı, şifre, vb.) güvenli bir şekilde alır.

#### İçerik
- load_dotenv(): .env dosyasındaki ortam değişkenlerini yükler.
- DATABASE_URL: PostgreSQL veritabanına bağlanmak için gereken bağlantı URL'sini oluşturur.

#### Kullanım

Ortam Değişkenleri: Bu dosya, veritabanı bağlantı bilgilerini bir .env dosyasından alır. Bu dosyada şunlar bulunmalıdır:
  - db_user: Veritabanı kullanıcı adı
  - db_password: Veritabanı şifresi
  - db_host: Veritabanı host adresi (varsayılan olarak localhost kullanılır)
  - db_port: Veritabanı portu (varsayılan olarak 5432 kullanılır)
  - db_name: Veritabanı adı

### *models.py*
Bu dosya, Pydantic modellerini tanımlar. Pydantic, veri doğrulama ve serileştirme işlemleri için kullanılan bir Python kütüphanesidir. Burada, veritabanındaki veri yapılarına uygun şekilde modeller oluşturulmuş ve API aracılığıyla bu verilerin düzgün bir şekilde doğrulanması sağlanmıştır.

#### İçerik
- OrderPydantic: Sipariş bilgilerini içeren veri modeli. Veritabanındaki orders tablosuyla ilişkilidir.
- OrderDetailPydantic: Sipariş detaylarını içeren veri modeli. Veritabanındaki order_details tablosuyla ilişkilidir.
- ProductPydantic: Ürün bilgilerini içeren veri modeli. Veritabanındaki products tablosuyla ilişkilidir.
- CustomerPydantic: Müşteri bilgilerini içeren veri modeli. Veritabanındaki customers tablosuyla ilişkilidir.
- CategoryPydantic: Kategori bilgilerini içeren veri modeli. Veritabanındaki categories tablosuyla ilişkilidir.
- PredictSalesRequestPydantic: Satış tahmini için gerekli parametreleri içeren veri modeli.
- PredictSalesResponsePydantic: Satış tahmini sonuçlarını içeren veri modeli.
- TrainModelResponsePydantic: Model eğitim işleminin yanıtı için veri modeli.
- MonthlySalesItemPydantic: Aylık satış özetini içeren veri modeli.
- ProductSalesItemPydantic: Ürün bazlı satış özetini içeren veri modeli.
- PredictionInputPydantic: Tahmin için kullanılacak giriş verilerini içeren veri modeli.

#### Kullanım
- Pydantic ile doğrulama sağlanır. Bu sayede API'ye gönderilen verilerin doğruluğu garanti altına alınır.
- Her sınıf, JSON formatında verilerin doğruluğunu kontrol etmek ve uygun şekilde serileştirmek için kullanılır.

### *schemas.py*
Bu dosya, SQLAlchemy'nin Base sınıfını kullanarak veritabanı modellerini tanımlar. Her bir model, veritabanındaki bir tabloyu temsil eder ve SQLAlchemy ile veritabanı üzerinde işlemler yapılmasına olanak sağlar.

#### İçerik
- OrdersModel: Siparişleri temsil eden model. orders tablosuna karşılık gelir.
- OrderDetailsModel: Sipariş detaylarını temsil eden model. order_details tablosuna karşılık gelir.
- ProductsModel: Ürünleri temsil eden model. products tablosuna karşılık gelir.
- CustomersModel: Müşterileri temsil eden model. customers tablosuna karşılık gelir.
- CategoriesModel: Kategorileri temsil eden model. categories tablosuna karşılık gelir.

#### Kullanım
- SQLAlchemy modelleri ile veritabanındaki tablolara erişebilir ve veri ekleyebilir, güncelleyebilir ya da silebilirsiniz.
- Her sınıf, veritabanındaki bir tabloyu temsil eder ve tabloların sütunları Column sınıfıyla tanımlanır.

### *utils.py*
Bu dosya, veri işleme sırasında kullanılan yardımcı fonksiyonları içerir. pandas kütüphanesi ile veri üzerinde çeşitli işlemler yapmaya yardımcı olacak fonksiyonlar bulunmaktadır.

#### İçerik
- clean_dataframe: Bu fonksiyon, pandas DataFrame'indeki eksik (NaN veya None) değerleri temizler ve her bir sütunun veri tipine göre uygun bir değeri atar.

---

##  Kurulum ve Çalıştırma

### 1. Reposu Klonla

git clone https://github.com/busraeskara/SalesPredictProject.git 

cd SalesPredictProject

### 2. Ortamı Hazırlama

Python 3.9+ yüklü olmalıdır.

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

### 3. Veriyi Yükleme ve Önişlem

main.py dosyasında veri keşfi, ön işleme ve model eğitimi yapılmaktadır.

Model dosyası decision_tree_model.pkl olarak kaydedilir.

### 4. API'yi Başlatma

uvicorn main:app --reload

API varsayılan olarak http://127.0.0.1:8000 adresinde yayına girer.

---

## API Kullanımı
API'yi test etmek için Swagger UI'yi veya Postman'i kullanabilirsiniz. Swagger UI, API dokümantasyonunu ve testini kolayca yapmanıza olanak sağlar.

### Swagger UI:

API dokümantasyonu otomatik olarak http://127.0.0.1:8000/docs adresinden erişilebilir.

### /predict Endpoint (Postman)

POST/predict

İstek (Örnek):

```json
{
  "order_date": "1997-04-11",
  "product_id": 1,
  "order_month": 7,
  "order_dayofweek": 0,
  "order_is_weekend": 0
}
```

Yanıt:

```json
{
    "predicted_sales": 15.0
}
```

---

## Proje Durumu

Proje tamamlanmıştır ve tahmin için kullanıma hazırdır. Yeni iyileştirmeler ve modeller ile güncellenebilir.

---

## Notlar
- Model basit bir regresyon modeli olarak tasarlanmıştır. Daha karmaşık senaryolarda farklı algoritmalar denenebilir.
- Proje eğitim amaçlıdır. Gerçek üretim ortamlarında uygun güvenlik, veri temizliği ve model değerlendirme süreçleri eklenmelidir.

---

## Teşekkürler

Bu projeyi incelediğiniz için teşekkür ederim!

Her türlü geri bildirim ve katkıya açığım.

Katkıda bulunmak isterseniz, pull request gönderebilirsiniz.
