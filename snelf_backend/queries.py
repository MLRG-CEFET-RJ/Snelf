from pathlib import Path
import sqlite3
import pandas as pd
import psycopg2
import pdb
from datetime import datetime
import random
from infra.DBConnection import DBConnection

db = DBConnection()


def insert_produtos():
    global db

    sql_query = f"""select distinct descricaoproduto, clean
                    from transactions"""

    db.cursor.execute(sql_query)

    medicine_transactions_consulted = db.cursor.fetchall()

    medicines_object = []
    inputProductsArray = []
    for transaction in medicine_transactions_consulted:
        transaction = list(transaction)
        transaction[0] = transaction[0].replace('\'','')
        print(transaction[0])
        transaction[1] = transaction[1].replace('\'','')
        transaction = tuple(transaction)
        inputProductsArray.append((str(transaction[1]), str(transaction[0])))

    args_products = ','.join(f"{i}" for i in inputProductsArray)

    sql_products = "INSERT INTO produtos(clean,description) VALUES "
    db.cursor.execute(sql_products + (args_products))

    db.connection.commit()
    print('Produtos inseridos com sucesso!')


def insert_products_transactions():
    global db

    sql_query = f"""select distinct p.id as productid, t.id transactionid
                    from transactions t 
                    join produtos p on p.description = t.descricaoproduto"""

    db.cursor.execute(sql_query)

    transactions_products_consulted = db.cursor.fetchall()

    print('Chegou em products_transactions')

    input_products_transactions_array = []
    for element in transactions_products_consulted:
        input_products_transactions_array.append(element)

    args_products_transactions = ','.join(f"{i}" for i in input_products_transactions_array)

    # print(args_products_transactions)

    sql_products = "INSERT INTO products_transactions(id_product,id_transaction) VALUES "
    db.cursor.execute(sql_products + (args_products_transactions))

    db.connection.commit()
    print('Products_transactions inseridos com sucesso!')


def insert_classes():
    global db

    classes = []
    with open('classes.txt', 'r') as f:
        classes = f.readlines()
    # print(classes)
    
    args_classes = ','.join(f"{i}" for i in classes)
    # print(args_classes)

    sql_products = "INSERT INTO classes(class_label) VALUES "
    db.cursor.execute(sql_products + args_classes)

    db.connection.commit()
    print('Classes inseridas com sucesso!')


def insert_products_classes():
    global db

    get_max = """select max(c.id) from classes c"""
    db.cursor.execute(get_max)
    max = db.cursor.fetchall()[0][0]

    get_min = """select min(c.id) from classes c"""
    db.cursor.execute(get_min)
    min = db.cursor.fetchall()[0][0]

    sql_get_all_products = """select p.id from produtos p"""
    db.cursor.execute(sql_get_all_products)
    product_ids = db.cursor.fetchall()

    input_products_classes_array = []
    for product_id in product_ids:
        input_products_classes_array.append((product_id[0], random.randint(min, max),'training'))

    # products_classes = []
    # with open('products_classes.txt', 'r') as f:
    #     products_classes = f.readlines()
    # print(products_classes)

    
    args_products_classes = ','.join(f"{i}" for i in input_products_classes_array)
    print(args_products_classes)

    sql_products_classes = """INSERT INTO products_classes(id_produto,id_classe,association_type) VALUES """
    db.cursor.execute(sql_products_classes + (args_products_classes))

    db.connection.commit()
    print('Products_classes inseridas com sucesso!')
