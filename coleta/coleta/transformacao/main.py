import pandas as pd
import sqlite3
import datetime

df = pd.read_json('../../data/data.jsonl', lines=True)

pd.options.display.max_columns = None
#adicionar a coluna source com o valor fixo
df['source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
df['data_coleta'] = datetime.datetime.now()

df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100


df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'])

#Conectar ao banco de dados
conn = sqlite3.connect('../../data/quotes.db')

df.to_sql('mercadoliv_items', conn, if_exists='replace', index=False)

conn.close()

print(df.head())