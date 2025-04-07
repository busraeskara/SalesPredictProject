# 📈 SalesPredictProject

Bu proje, **Northwind veritabanındaki** sipariş verilerini kullanarak ürün bazlı satış tahmini yapan bir makine öğrenmesi modelini REST API aracılığıyla erişilebilir hale getirmektedir. Dış sistemler bu API'yi kullanarak belirli ürünlere ait satış tahminleri alabilir. Python, FastAPI, PostgreSQL, scikit-learn gibi modern araçlar kullanılarak geliştirilmiştir. 

> **Amaç:** Gelecekteki ürün taleplerini tahmin ederek işletmelerin daha doğru kararlar almasını sağlamak.


---

## Özellikler

- Ürün geçmiş verilerine göre satış tahmini yapar
- RESTful API mimarisi  
- PostgreSQL veritabanı bağlantısı  
- Model eğitimi ve tahmin endpoint’leri    
- Swagger UI ile API dokümantasyonu
- Zaman serisi ve kategorik özellik mühendisliği  
- MAE, MSE, RMSE, R² gibi metriklerle değerlendirme 

---

## Kullanılan Teknolojiler

- Python, FastAPI, SQLAlchemy
- scikit-learn (DecisionTreeRegressor)
- PostgreSQL, Pydantic, Uvicorn
- Pandas, NumPy, Joblib
- Swagger UI / Postman 

---

## Proje Yapısı

SalesPredictProject/ ├── main.py ├── database.py ├── config.py ├── models.py ├── schemas.py ├── utils.py ├── requirements.txt ├── README.md ├── decision_tree_model.pkl ├── openapi.json

---

## Dosyaların Açıklamaları

### [main.py](./main.py) – API ve Model Entegrasyon Katmanı
Bu dosya, projenin ana uygulama dosyasıdır ve aşağıdaki temel işlevleri yerine getirir:

- FastAPI sunucusunu başlatır  
- Swagger UI ile otomatik dökümantasyon: `http://localhost:8000/docs`  
- Model eğitimi:  
  - `/train_model` endpoint’i ile başlatılır  
  - Veriler `StandardScaler` ile ölçeklenir  
  - Model `decision_tree_model.pkl` olarak kaydedilir  
- Tahmin işlemi:  
  - `/predict` endpoint’i  
  - MAE, MSE, RMSE, R² metrikleri kullanılır  
- GET endpoint’leri: `/orders`, `/products`, `/categories`, vb.  
- Özet endpoint’ler: `/monthly_sales_summary`, `/product_sales_summary`  
- Özellik mühendisliği, hata yönetimi, logging

### [database.py](./database.py) 
Bu dosya, veritabanı bağlantısını yönetmek ve veritabanından veri çekmek için kullanılan yardımcı fonksiyonları içerir. 

- SQLAlchemy ile PostgreSQL bağlantısı  
- `fetch_table(table_name)`: Veritabanı tablolarını Pandas DataFrame olarak döndürür  
- `engine`, `SessionLocal`, `Base` bileşenleri yer alır  

### [config.py](./config.py) 
Bu dosya, veritabanı bağlantı bilgilerini yükler ve ortam değişkenlerinden alır.

- .env dosyasından veritabanı bilgilerini çeker  
- `DATABASE_URL` oluşturulur  
- Ortam değişkenleri:
  - `db_user`, `db_password`, `db_host`, `db_port`, `db_name`  

### [models.py](./models.py)
- Pydantic modelleri  
- API giriş-çıkış verilerinin doğrulanmasını sağlar  
- Örnek modeller: `OrderPydantic`, `ProductPydantic`, `PredictSalesRequestPydantic`, vb.

### [schemas.py](./schemas.py)

- SQLAlchemy ORM sınıfları  
- Veritabanı tablolarını temsil eder: `OrdersModel`, `ProductsModel`, vb.  

### [utils.py](./utils.py)
- Yardımcı veri işleme fonksiyonları  
- Örnek: `clean_dataframe` — NaN değerleri uygun şekilde temizler  

---

##  Kurulum ve Çalıştırma

### 1. Reposu Klonlayın
```bash
git clone https://github.com/busraeskara/SalesPredictProject.git 

cd SalesPredictProject
```

### 2. Ortamı Oluşturun
```bash
python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Veritabanını Ayarları
.env dosyası oluşturun ve içerisine şunları yazın:
```env
db_user = postgres
db_password = yourpassword
db_host = localhost
db_port = 5432
db_name = GYK2Northwind
```

### 4. API'yi Başlatın
```bash
uvicorn main:app --reload
```

### 5. Swagger UI ile Test Edin
📌 http://localhost:8000/docs

---

## API Kullanımı
API'yi test etmek için Swagger UI'yi veya Postman'i kullanabilirsiniz. Swagger UI, API dokümantasyonunu ve testini kolayca yapmanıza olanak sağlar.

### Tahmin Endpoint'i 
####  Endpoint: POST /predict

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
Swagger veya Postman ile kolayca test edebilirsiniz.

## 📌 Proje Durumu

Proje tamamlanmıştır ve tahmin için kullanıma hazırdır. Yeni iyileştirmeler ve model alternatifleri eklenebilir

---

## Notlar
- Model basit bir regresyon modeli olarak tasarlanmıştır. Daha karmaşık senaryolarda farklı algoritmalar denenebilir.
- Proje eğitim amaçlıdır. Gerçek üretim ortamlarında uygun güvenlik, veri temizliği ve model değerlendirme süreçleri eklenmelidir.

---

## Teşekkürler

Bu projeyi incelediğiniz için teşekkür ederim!

Her türlü geri bildirim ve öneriye açığım. 😊

🤝Katkıda bulunmak isterseniz:
1. Forklayın
2. Yeni bir branch oluşturun
3. Değişiklikleri yapın
4. Pull request gönderin
