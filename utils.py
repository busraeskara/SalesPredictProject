import pandas as pd


# DataFrame'deki NaN veya None değerlerini temizleme işlemi
# Bu fonksiyon, DataFrame'deki NaN veya None değerlerini temizler ve uygun türlere dönüştürür.
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].fillna("N/A").astype(str)
        elif pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].fillna(0).astype(int)
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].fillna(0.0).astype(float)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            # Eğer timestamp varsa stringe çevir
            df[col] = df[col].fillna(pd.Timestamp("1970-01-01")).astype(str)
        else:
            # Diğer türler için de stringe çevirip 'N/A' ata
            df[col] = df[col].fillna("N/A").astype(str)
    return df