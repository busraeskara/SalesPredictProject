from typing import List
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from fastapi import Body, FastAPI, HTTPException,APIRouter
import warnings
import logging

import database as database
import models as models
import utils as utils

#2.2 Fonksiyonel Gereksinimler

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Northwind API", description="Northwind API", version="1.0")

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

logging.basicConfig(level=logging.INFO)

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


#Gerekli veri ön işleme adımları yapılacak.

@app.get("/orders", response_model=List[models.OrderPydantic], summary="Sipariş Listesi", description="Müşterilerin siparişlerini listeler.", tags=["Siparişler"],  responses={
    200: {"description": "Successful"},
    404: {"description": "Order not found"},
    500: {"description": "Server error"}
})
def get_orders():
    try:
        df = database.fetch_table("orders")
        if df.empty:
            raise HTTPException(status_code=404, detail="Sipariş bulunamadı.")
        # NaN veya None değerlerini kontrol etme ve yerine varsayılan değer atama
        df = utils.clean_dataframe(df)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Orders çekilirken hata: {e}")
        raise HTTPException(status_code=500, detail="Siparişler alınırken bir hata oluştu.")

@app.get("/order_details", response_model=List[models.OrderDetailPydantic], summary="Sipariş Detayı", description="Siparişlerin detaylarını listeler.", tags=["Sipariş Detayı"],  responses={
    200: {"description": "Successful"},
    404: {"description": "Order details not found"},
    500: {"description": "Server error"}
})
def get_order_details():
    try:
        df = database.fetch_table("order_details")
        if df.empty:
            raise HTTPException(status_code=404, detail="Sipariş detayı bulunamadı.")
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Order_Details çekilirken hata: {e}")
        raise HTTPException(status_code=500, detail="Sipariş detayı alınırken bir hata oluştu.")

@app.get("/products", response_model=List[models.ProductPydantic], summary="Ürün Listesi", description="Ürünleri listeler.", tags=["Ürünler"],  responses={
    200: {"description": "Successful"},
    404: {"description": "Products not found"},
    500: {"description": "Server error"}
})
def get_products():
    try:
        df = database.fetch_table("products")
        if df.empty:
            raise HTTPException(status_code=404, detail="Ürün bilgisi bulunamadı.")
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Products çekilirken hata: {e}")
        raise HTTPException(status_code=500, detail="Ürünler alınırken bir hata oluştu.")

@app.get("/customers", response_model=List[models.CustomerPydantic], summary="Müşteri Listesi", description="Müşterileri listeler.", tags=["Müşteriler"],  responses={
    200: {"description": "Successful"},
    404: {"description": "Customers not found"},
    500: {"description": "Server error"}
})
def get_customers():
    try:
        df = database.fetch_table("customers")
        if df.empty:
            raise HTTPException(status_code=404, detail="Müşteri bilgisi bulunamadı.")
        # None veya NaN olan alanlara varsayılan değer atama
        df = utils.clean_dataframe(df)
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Customers çekilirken hata: {e}")
        raise HTTPException(status_code=500, detail="Müşteriler alınırken bir hata oluştu.")

@app.get("/categories", response_model=List[models.CategoryPydantic], summary="Kategori Listesi", description="Ürün kategorilerini listeler.", tags=["Kategoriler"],  responses={
    200: {"description": "Successful"},
    404: {"description": "Categories not found"},
    500: {"description": "Server error"}
})
def get_categories():
    try:
        df = database.fetch_table("categories")
        if df.empty:
            raise HTTPException(status_code=404, detail="Kategori bilgisi bulunamadı.")
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Categories çekilirken hata: {e}")
        raise HTTPException(status_code=500, detail="Kategori alınırken bir hata oluştu.")



#Ürün bazlı geçmiş satış verilerine göre tahmin modeli oluşturulacak.

# Veriyi birleştir ve yeni özellikler ekle
def sales_merge():
    orders = database.fetch_table("orders")
    order_details = database.fetch_table("order_details")
    #print(order_details.columns)
    products = database.fetch_table("products")
    df = pd.merge(orders, order_details, on="order_id")
    df = pd.merge(df, products, on="product_id", suffixes=('_order_details', '_products'))

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["timestamp"] = df["order_date"].astype("int64") / 10**9  # Tarih dönüşümü düzeltildi

    # Yeni özellikler ekleyelim (Modelin öğrenmesini kolaylaştırmak için order_date verisini kullanarak aşağıdaki kolonları oluşturduk.) -> Özellik Mühendisliği
    df['order_month'] = df['order_date'].dt.month
    df['order_dayofweek'] = df['order_date'].dt.dayofweek
    df['order_is_weekend'] = df['order_dayofweek'].apply(lambda x: 1 if x >= 5 else 0)

    #print(df.columns)
    df['unit_price'] = df['unit_price_order_details']  # order_details tablosundaki unit_price kullanılıyor
    df.drop(['unit_price_order_details', 'unit_price_products'], axis=1, inplace=True)
    df = df.dropna()  # Satırdaki eksik verileri kaldır
    return df


# Veriyi ölçeklendirme (Scaling)
def scale_data(df):
    scaler = StandardScaler()
    df[['timestamp']] = scaler.fit_transform(df[['timestamp']])
    return df

# Decision Tree modelini eğitme
def train_decision_tree(df):
    # X ve y'yi belirleyin
    print(df)
    X = df[["timestamp", "product_id", "order_month", "order_dayofweek", "order_is_weekend"]]
    y = df["quantity"]

    # Sütun isimlerini düzgün bir şekilde string'e dönüştür
    X.columns = [str(col) for col in X.columns]  # Her sütun ismini string'e çevir

    # Eğitim ve test setlerine ayırın
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modeli oluşturun ve eğitin
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Modeli kaydedin
    joblib.dump(model, "decision_tree_model.pkl")

    return model


# Model parametre ayarını yapma (GridSearchCV) - Decision Tree için
def tune_model(X_train, y_train):
    param_grid_tree = {
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
    }


    grid_search_tree = GridSearchCV(DecisionTreeRegressor(random_state=42), param_grid_tree, cv=3, n_jobs=-1)

    grid_search_tree.fit(X_train, y_train)


    print(f"Best Parameters for Decision Tree: {grid_search_tree.best_params_}")


    return grid_search_tree.best_estimator_

# Performans değerlendirmesi (MAE, MSE, R2)

def evaluate_model(model, X_test, y_test):
    # X_test'in sütun adlarını string'e dönüştürme
    X_test.columns = [str(col) for col in X_test.columns]

    # Modelin tahminlerini yap
    y_pred = model.predict(X_test)

    # Performans değerlendirmesi
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R^2: {r2}")

@app.post("/predict", response_model=models.PredictSalesResponsePydantic, summary="Satış Tahmini", description="Verilen ürün ve tarih için satış tahmini yapar.", tags=["Tahmin"])
def predict_sales(data: models.PredictSalesRequestPydantic = Body(...)):
    try:
        model = joblib.load("decision_tree_model.pkl")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model dosyası bulunamadı.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model yükleme hatası: {str(e)}")

    try:
        order_date = pd.to_datetime(data.order_date).timestamp()
        prediction = model.predict([[order_date, data.product_id, data.order_month, data.order_dayofweek, data.order_is_weekend]])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Tahmin yapılamadı: {str(e)}")

    return models.PredictSalesResponsePydantic(predicted_sales=prediction[0])


# Veriyi birleştir
df = sales_merge()

# Özellik mühendisliği ve ölçekleme
df = scale_data(df)

# Modeli eğit (Decision Tree)
model_tree = train_decision_tree(df)

# Modelin başarımını değerlendirin
X_train, X_test, y_train, y_test = train_test_split(df[["timestamp", "product_id", "order_month", "order_dayofweek", "order_is_weekend"]], df["quantity"], test_size=0.2, random_state=42)
evaluate_model(model_tree, X_test, y_test)

#modelin eğitilmesini API üzerinden tetikleme.

@app.post("/train_model", response_model=models.TrainModelResponsePydantic, summary="Model Eğitimi", description="Modeli eğitir ve kaydeder.", tags=["Model Eğitimi"])
def train_model():
# Veriyi birleştir ve hazırlık işlemlerini yap
    df = sales_merge()
    # Özellik mühendisliği ve ölçekleme
    df = scale_data(df)
    print(df)
    # Modeli eğit (Decision Tree)
    model_tree = train_decision_tree(df)

    # Modelin başarımını değerlendirin
    X_train, X_test, y_train, y_test = train_test_split(df[["timestamp", "product_id", "order_month", "order_dayofweek", "order_is_weekend"]], df["quantity"], test_size=0.2, random_state=42)
    evaluate_model(model_tree, X_test, y_test)

    return models.TrainModelResponsePydantic(message="Model eğitildi ve kaydedildi.")


# Aylık satış özeti
def monthly_sales_summary():
    # Veriyi al
    df = sales_merge()

    # "order_date" sütununu tarih formatına çevir
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Aylık bazda gruplama
    df['order_year_month'] = df['order_date'].dt.to_period('M')

    # Aylık satış özetini oluştur: toplam satış miktarı ve toplam tutar
    monthly_summary = df.groupby('order_year_month').agg(
        total_sales=('quantity', 'sum'),
        total_revenue=('unit_price', 'sum')  # Burada unit_price'i kullandık
    ).reset_index()

    monthly_summary.rename(columns={'order_year_month': 'month'}, inplace=True)
    monthly_summary['month'] = monthly_summary['month'].astype(str)

    return monthly_summary

# Ürün bazlı satış özeti
def product_sales_summary():
    # Veriyi al
    df = sales_merge()

    # Ürün bazında gruplama
    product_summary = df.groupby('product_id').agg(
        total_sales=('quantity', 'sum'),
        total_revenue=('unit_price', 'sum')
    ).reset_index()

    # Ürün ismini de ekleyelim
    product_summary = product_summary.merge(database.fetch_table("products")[['product_id', 'product_name']], on='product_id', how='left')

    return product_summary[['product_id', 'product_name', 'total_sales', 'total_revenue']]

@app.get("/monthly_sales_summary", response_model=List[models.MonthlySalesItemPydantic], summary="Aylık Satış Özeti", description="Aylık satış özetini döndürür.", tags=["Satış Özeti"])
def get_monthly_sales_summary():
    try:
        # Aylık satış özetini al
        summary = monthly_sales_summary()
        return summary.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/product_sales_summary", response_model=List[models.ProductSalesItemPydantic], summary="Ürün Bazlı Satış Özeti", description="Ürün bazında satış özetini döndürür.", tags=["Satış Özeti"])
def get_product_sales_summary():
    try:
        # Ürün bazlı satış özetini al
        summary = product_sales_summary()
        return summary.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


#Özellik mühendisliği:
#ürün fiyatı, müşteri segmentasyonu gibi özellikler üretme

#ürün fiyatının kategorik özelliklere dönüştürülmesi
def price_category(row):
    if row['unit_price'] < 10:
        return 'low'
    elif 10 <= row['unit_price'] < 50:
        return 'medium'
    else:
        return 'high'

df['price_category'] = df.apply(price_category, axis=1)

#Müşteri segmantasyonu için:
#Her müşteri için en çok satın alınan kategori
customer_category = df.groupby('customer_id')['category_id'].agg(lambda x: x.mode()[0]).reset_index()
customer_category.rename(columns={'category_id': 'favorite_category'}, inplace=True)

#Bu özelliği veri setine ekleme
df = df.merge(customer_category[['customer_id', 'favorite_category']], on='customer_id', how='left')