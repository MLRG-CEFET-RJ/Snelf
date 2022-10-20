from pathlib import Path
import sqlite3
import pandas as pd
import psycopg2
import pdb
from datetime import datetime
from pre_processamento import inicia_pre_processamento
import asyncio
from importar_csv_para_sql import get_all_medicine_expanded_df, fill_classes_table, get_all_medicine_df, fill_products_classes_table

# Testes de importação e rodagem do modelo de IA
# from pre_processamento import inicia_pre_processamento

# inicia_pre_processamento('./dados/produtos_farmaceuticos.csv')


# (OK) Testes para pegar todos os dados do BD e colocar em um DataFrame
# connection = psycopg2.connect(database="testejp", user="testejp", password="testejp", host="localhost", port="5432")
# connection.autocommit=True
# cursor = connection.cursor()
# sql_table_creation = "SELECT mt.DescricaoProduto, mt.CLEAN FROM medicine_transactions mt"
# cursor.execute(sql_table_creation)

# medicine_transactions_records = cursor.fetchall()
# medicine_transactions_dataframe = pd.DataFrame(medicine_transactions_records, columns=["DescricaoProduto","CLEAN"])
# print(medicine_transactions_dataframe)

# connection.commit()
# connection.close()



# loop = asyncio.get_event_loop()
# forecast = loop.run_until_complete(inicia_pre_processamento())
# loop.close()

# def testagem():
#     import os
#     os.system('python3 ./data_augmentation.py "./dados/medicamentos.csv" "./dados/medicamentos_aumentado.csv" medicamentos 1')


#from fastText.python.fasttext_module.fasttext.FastText import _FastText as fasttext
import fasttext
from matplotlib.pyplot import text

# model = fasttext.train_supervised('dados/data.train.txt')
# # texto = ['CIPROFIBRATO']
# texto = ['amoxicilina']
# teste = model.predict(texto[0])
# print (teste)


# fill_classes_table()
# get_all_medicine_df()
# fill_products_classes_table()

# model = fasttext.supervised('dados/data.train.txt','modelo/modelo')
model = fasttext.train_supervised('dados/data.train.txt')
teste = model.predict('DEXAMETASONA', k=1)
# teste = model.predict_proba('Teste',k=1)

print(teste)
