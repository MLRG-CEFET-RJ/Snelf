import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from http.client import HTTPException
from fastapi import Body, FastAPI, File, UploadFile, Query, Request
from fastapi.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from treinamento import Treinamento
from pre_processamento import inicia_pre_processamento
import fasttext 
from importar_csv_para_sql import fill_db_tables, insert_transactions, get_medicines_from_label, getTransactionsFromClean, get_transactions_from_product
import pdb
import unittest
import numpy as np
from fastapi.openapi.utils import get_openapi
import debugpy

debugpy.listen(("0.0.0.0", 5678))  # Altere a porta para 5678 ou outra disponível
print("Aguardando o depurador se conectar...")
debugpy.wait_for_client()

# Após o depurador se conectar, você pode ativar o ponto de interrupção
print("Depurador conectado.")


app = FastAPI(debug=True)
treinamento = Treinamento()

@app.get("/openapi.json")
async def get_open_api_endpoint():
    return get_openapi(title="Documentação do API", version="1.0", routes=app.routes)

#rota de importação do csv. estudando como fazer para upload em csv maior
@app.post("/importarCsv")
async def importarCsv():
    csvFile = './dados/medicamentos.csv'
    if True:
        #modifica o csv para formato que é aceito no treinamento
        # cleaned_dataset = clean_dataset(csvFile)
        #aqui seria a chamada para a api do modelo, iniciando o pré processamento
        await inicia_pre_processamento()
        fasttext.supervised('dados/data.train.txt','modelo/modelo')

        print("Arquivo recebido na API de importação")
        return {"filename": csvFile.filename, "status":"Arquivo recebido na API de importação"}
    else:
        raise HTTPException(status_code=422, detail="Formato de arquivo não suportado")

@app.post("/treinarModelo")
def treinamentoModelo():
    try:
        fill_db_tables()
        # await inicia_pre_processamento()
        # fasttext.supervised('dados/data.train.txt','modelo/modelo')
        return {"status":"Treinamento do modelo realizado com sucesso."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Modelo não pôde ser treinado.")

@app.post("/consultarGrupo")
async def consultaGrupo(busca: str = Body(...)):
    try:
        array_from_product = get_transactions_from_product(busca)
        transactions = array_from_product
        
        model = fasttext.load_model("modelo/modelo.bin")
        label = model.predict_proba([busca],k=1)[0][0][0]
        
        array_from_prediction = get_medicines_from_label(label)
        # transactions = array_from_product + array_from_prediction[0:100]

        # print(label)
        # print(transactions)
        return { 'medicines': transactions }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Consulta não pôde ser realizada.")

@app.post("/consultarClean")
async def consultaClean(busca: str = Body(...)):
    try:
        transactions = getTransactionsFromClean(busca)
        print(len(transactions))
        return { 'medicines': transactions }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="Consulta não pôde ser realizada.")

# rota de importação do csv. estudando como fazer para upload em csv maior
# @app.post("/importarMedicamentos")
# async def importarMedicamentos(csvFile: UploadFile = File(...)):
#     if csvFile.filename.endswith('.csv'):
#         insert_medicine(csvFile)
#         return {"filename": csvFile.filename, "status":"Arquivo importado com sucesso."}
#     else:
#         raise HTTPException(status_code=422, detail="Formato de arquivo não suportado")

@app.get("/teste")
async def root():
    return "Teste executado com sucesso."


#tá executando esse aqui na importação do csv
@app.post("/importarTransacoes")
async def importarTransacoes(csvFile: UploadFile = File(...)):
    if csvFile.filename.endswith('.csv'):
        insert_transactions(csvFile)
        fill_db_tables()
        print("Arquivo importado com sucesso.")
        return {"filename": csvFile.filename, "status":"Arquivo importado com sucesso."}
    else:
        raise HTTPException(status_code=422, detail="Formato de arquivo não suportado")

historico_status = []

@app.post("/treinar-modelo-de-verdade")
async def treinarModeloDeVerdade(forceRestart: bool = False):
    """
    Inicia/Retoma o treinamento do modelo.

    :param forceRestart: Indica se o treinamento deve ser reiniciado do zero (True) ou continuar de onde parou (False).
    :type forceRestart: bool
    :return: Texto informativo. "Treinamento iniciado" ou  "Já existe um treinamento em andamento"
    :rtype: str

    Utiliza a função :meth:`treinamento.Treinamento.estaEmTreinamento` para verificar se existe um treinamento em andamento

    Utiliza a função :meth:`treinamento.Treinamento.iniciarTreinamento` para iniciar o treinamento
    """

    localDir = os.path.dirname(os.path.abspath(__file__))
    try:
        if not treinamento.estaEmTreinamento():
            treinamento.iniciarTreinamento(forceRestart=True)
            #print(historico_status)
            return "Treinamento iniciado"
        else:
            return "Já existe um treinamento em andamento"

    except Exception as ex:
        os.chdir(localDir)
        raise HTTPException(status_code=422, detail=ex)


@app.post("/parar-treinamento")
async def pararTreinamento():
    """
    Para o treinamento do modelo

    Utiliza a função :meth:`treinamento.Treinamento.pararTreinamento` que parar o treinamento que está em andamento
    """

    try:
        treinamento.pararTreinamento()
        return "Treinamento parado"

    except Exception as ex:
        print(ex)
        return
        # raise HTTPException(ex, status_code=422, detail=ex)



@app.get("/obter-status-treinamento")
async def obterStatusTreinamento():
    try:
        #historico_status.append(treinamento.obterStatusTreinamento())
        return treinamento.obterStatusTreinamento()  #concatenar as linhas de "log.txt - preprocessamento" com "model.txt - treinamento" e trazer tudo pra cá e lutar para mostrar isto no front bonitinho
    except Exception as ex:
        raise HTTPException(status_code=422, detail=ex)


#burlando cors
app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)