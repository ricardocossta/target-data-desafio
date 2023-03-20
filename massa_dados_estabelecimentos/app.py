import pandas as pd
import pymongo
from elasticsearch import Elasticsearch
import os.path

client = pymongo.MongoClient("mongodb://localhost:27017", username='root', password='root')
db = client["estabelecimentosdb"]
collection = db["estabelecimentos"]

my_path = os.path.abspath(os.path.dirname(__file__))
csv_file_path = my_path + "\\dados.csv"

es = Elasticsearch(['http://localhost:9200/'])

df = pd.read_csv(csv_file_path, sep=';', encoding="utf-8", encoding_errors='replace',header=None, usecols=[0, 1, 2, 4, 18, 21, 22, 27], nrows=20)
df = df.dropna().reset_index(drop=True)

df.rename(columns={0: 'CNPJ Basico', 1: 'CNPJ Ordem', 2: 'CNPJ DV', 4: 'Nome Fantasia', 18: 'CEP', 21: 'DDD 1',
                   22: 'TELEFONE 1', 27: 'Email'}, inplace=True)

df = df.head(10)
df['CNPJ COMPLETO'] = df['CNPJ Basico'].astype(str) + df['CNPJ Ordem'].astype(str) + df['CNPJ DV'].astype(str)
df['Telefone'] = df['DDD 1'].astype(str) + df['TELEFONE 1'].astype(str)

df = df.loc[:, ['CNPJ COMPLETO', 'Nome Fantasia', 'CEP', 'Telefone', 'Email']]

print("Data Frame Inserido:")
print(df)


for index, row in df.iterrows():
    data = {
        'CNPJ': row["CNPJ COMPLETO"],
        'NomeFantasia': row["Nome Fantasia"],
        'CEP': row["CEP"],
        'Telefone': row["Telefone"],
        'Email': row["Email"]
    }
    es.index(index='estabelecimentos', document=data, id=index + 1)
    collection.insert_one(data)

print("Dados inseridos no Mongodb e Elasticsearch com sucesso!")
