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

```bash
SalesPredictProject/
├── data/                    # Northwind veritabanı ve veri işleme dosyaları
│
├── model/                   # Model eğitimi ve kayıt işlemleri
│
├── docs/                    # Dokümantasyon dosyaları (Swagger / Postman)
│   ├── swagger.yaml         # Swagger API tanımı (isteğe bağlı)
│   └── SalesPredict.postman_collection.json  # Postman koleksiyonu
│
├── requirements.txt         # Proje bağımlılıkları
├── README.md                # Bu dosya
└── .gitignore

## ⚙️ Kurulum ve Çalıştırma

### 1. Reposu Klonla

```bash
git clone https://github.com/busraeskara/SalesPredictProject.git
cd SalesPredictProject
