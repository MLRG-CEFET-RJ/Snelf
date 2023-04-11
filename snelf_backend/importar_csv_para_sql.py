from pathlib import Path
import sqlite3
import pandas as pd
import psycopg2
import pdb
from datetime import datetime
from queries import insert_produtos, insert_products_transactions, insert_classes, insert_products_classes
from infra.DBConnection import DBConnection
db = DBConnection()

def fill_db_tables():
    print('Começou')
    insert_produtos()
    print('Inseriu produtos')
    insert_products_transactions()
    print('Inseriu products_transactions')
    insert_classes()
    print('Inseriu classes')
    insert_products_classes()
    print('Inseriu products_classes')


def insert_transactions(csvFile):
    global db
    
    cols = ["CodigoNFe","DataEmissao","MunicipioEmitente","unidadecomercial","quantidadecomercial","valorunitariocomercial","DescricaoProduto","CLEAN"]
    df = pd.read_csv(csvFile.file, usecols=cols, dtype={0:int, 1: str, 2:str, 3:str, 4:float, 5:float, 6:str, 7:str}, sep=',')
    
    inputArray = []

    iterative_string=""

    for index, row in df.iloc[0:len(df)].iterrows():
        # row = list(row)
        row.DescricaoProduto = row.DescricaoProduto.replace('\'','')
        row.MunicipioEmitente = row.MunicipioEmitente.replace('\'','')
        row.unidadecomercial = row.unidadecomercial.replace('\'','')
        row.CLEAN = row.CLEAN.replace('\'','')
        # row = tuple(row)
        inputArray.append((row.CodigoNFe, row.DataEmissao, row.MunicipioEmitente, row.unidadecomercial, row.quantidadecomercial, row.valorunitariocomercial, row.DescricaoProduto.replace('\'',''), row.CLEAN))
        iterative_string = iterative_string + "%s"
    
    iterative_string = iterative_string.replace("s%","s,%")
    
    args = ','.join(f"{i}" for i in inputArray)

    
    sql = "INSERT INTO transactions(CodigoNFe,DataEmissao,MunicipioEmitente,unidadecomercial,quantidadecomercial,valorunitariocomercial,DescricaoProduto,CLEAN) VALUES "
    
    
    db.cursor.execute(sql + (args))
    
    db.connection.commit()




# Método para população da Tabela classes
def fill_classes_table():
    global db
    
    inputArray = []
    
    training_file = open('./dados/data.train.txt', 'r')
    training_lines = training_file.readlines()
        
    for line in training_lines:
        inputArray.append((str(line.split()[0])))
        
    inputArray = list(set(inputArray))
    
    args = ','.join(f"('{i}')" for i in inputArray)
    sql = "INSERT INTO classes(class_label) VALUES "    
    db.cursor.execute(sql + (args))
    
    db.connection.commit()


def fill_products_classes_table():
    global db
    
    inputArray = []
    training_file = open('./dados/data.train.txt', 'r')
    training_lines = training_file.readlines()
    for line in training_lines:
        inputArray.append((str(line.split()[0]), str(line.replace(line.split()[0] + ' ', '').replace('\n',''))))
        
    inputArray = list(set(inputArray))
    
    pdb.set_trace()
    # sql = "select insert_in_products_classes_table"
    sql = "INSERT INTO "
    for input in inputArray:
        arg = str(input)
        print(sql + arg)
        db.cursor.execute(sql + arg)

    db.connection.commit()


def get_all_medicine_expanded_df():
    global db
    sql_table_creation = "SELECT mt.DescricaoProduto, mt.CLEAN FROM transactions mt"
    db.cursor.execute(sql_table_creation)

    medicine_transactions_records = db.cursor.fetchall()
    medicine_transactions_dataframe = pd.DataFrame(medicine_transactions_records, columns=["DescricaoProduto","CLEAN"])

    db.connection.commit()
    
    return medicine_transactions_dataframe

def getTransactionsFromClean(busca):
    global db
    sql_table_creation = f"""select *
                             from transactions t 
                             where clean like '%{busca}%'"""

    db.cursor.execute(sql_table_creation)

    medicine_transactions_consulted = db.cursor.fetchall()
    
    medicines_object = []
    for transaction in medicine_transactions_consulted:
        medicines_object.append({
            'id': transaction[0],
            'CodigoNFe': transaction[1],
            'DataEmissao': transaction[2],
            'MunicipioEmitente': transaction[3],
            'unidadecomercial': transaction[4],
            'quantidadecomercial': transaction[5],
            'valorunitariocomercial': transaction[6],
            'DescricaoProduto': transaction[7],
            'CLEAN': transaction[8]
        })

    print('medicines_object')
    print(medicines_object)

    db.connection.commit()
    
    return medicines_object

def get_transactions_from_product(busca):
    global db

    sql_table_creation = f"""select t.*
                            from transactions t
                            where LOWER(t.descricaoproduto) like LOWER('%{busca}%')"""

    db.cursor.execute(sql_table_creation)

    medicine_transactions_consulted = db.cursor.fetchall()
    
    medicines_object = []
    for transaction in medicine_transactions_consulted:
        medicines_object.append({
            'id': transaction[0],
            'CodigoNFe': transaction[1],
            'DataEmissao': transaction[2],
            'MunicipioEmitente': transaction[3],
            'unidadecomercial': transaction[4],
            'quantidadecomercial': transaction[5],
            'valorunitariocomercial': transaction[6],
            'DescricaoProduto': transaction[7],
            'CLEAN': transaction[8]
        })

    db.connection.commit()
    
    return medicines_object


def get_medicines_from_label(label):
    global db
    sql_table_creation = f"""select t.*
                            from products_classes pc
                            join classes c 
                                on c.id=pc.id_classe
                                and c.class_label like '%{label}%'
                            join products_transactions pt 
                                on pt.id_product=pc.id_produto
                            join transactions t
                                on t.id=pt.id_transaction"""

    db.cursor.execute(sql_table_creation)

    medicine_transactions_consulted = db.cursor.fetchall()
    
    medicines_object = []
    for transaction in medicine_transactions_consulted:
        medicines_object.append({
            'id': transaction[0],
            'CodigoNFe': transaction[1],
            'DataEmissao': transaction[2],
            'MunicipioEmitente': transaction[3],
            'unidadecomercial': transaction[4],
            'quantidadecomercial': transaction[5],
            'valorunitariocomercial': transaction[6],
            'DescricaoProduto': transaction[7],
            'CLEAN': transaction[8]
        })

    db.connection.commit()
    
    return medicines_object

def get_limited_medicines_with_clean():
    global db
    sql_table_creation = f"""select distinct descricaoproduto, clean
                             from transactions
                             where clean NOT in ('', 'N/I', '-1', '0')
                             order by clean desc
                             limit 1000"""

    db.cursor.execute(sql_table_creation)

    medicine_transactions_with_clean = db.cursor.fetchall()
    
    medicine_transactions_dataframe = pd.DataFrame(medicine_transactions_with_clean, columns=["DescricaoProduto","CLEAN"])

    print(medicine_transactions_dataframe)
    
    db.connection.commit()
    
    return medicine_transactions_dataframe

# get_limited_medicines_with_clean()
# fill_products_classes_table()