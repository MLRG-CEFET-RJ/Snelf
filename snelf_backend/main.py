import csv
from io import BytesIO, StringIO
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from typing import Optional

from fastapi.responses import StreamingResponse
import pandas as pd
from utils.files import ManipuladorDeArquivos
from modelos.http_model import HttpResponse
from pre_processamento import inicia_pre_processamento
from servicos.fasttext import ManipuladorFasttext
from servicos.medicamentos import MedicamentosServico
from servicos.suprimentos import SuprimentosServico
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
import uvicorn
from treinamento import Treinamento 

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
@app.get('/')
async def home():
    return {
        'TESTE': 'TESTE'
    }

"""
O post abaixo é usado para iniciar ou retormar o treinamento
- forceRestart: Indica se o treinamento deve ser reiniciado do zero (True) ou continuar de onde parou (False).
- csv_file: Arquivo a ser enviado para gerar o modelo, se não existir, usará o que está em /dados
"""
@app.post("/treinamento/treinar-modelo")
async def treinar_modelo(csv_file: Optional[UploadFile] = File(None), force_restart = False):
    try:
        if csv_file is not None:
            manipulador_de_arquivos = ManipuladorDeArquivos()
            await manipulador_de_arquivos.escrever_dados_treinamento_txt(csv_file=csv_file)
        
        """ 
        Descomente o trecho abaixo para treinar o modelo
        modelo = fasttext.train_supervised('dados/data.train.txt')
        print(modelo.labels)
        print(modelo.words)
        modelo.save_model('modelos/modelo_novo.bin') """
        manipulador_fasttext = ManipuladorFasttext()
        resposta_treinamento = manipulador_fasttext.iniciar_treinamento()
        
        if resposta_treinamento['erro']:
            texto = resposta_treinamento['texto']
            status = resposta_treinamento['status']
            return HTTPException(detail=texto, status_code=status)
        
        texto = resposta_treinamento['texto']
        status = resposta_treinamento['status']
        return {"texto": texto, "status": status}
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar iniciar o treinamento')

@app.get("/treinamento/parar-treinamento")
async def parar_treinamento():
    try:
        manipulador_fasttext = ManipuladorFasttext()
        manipulador_fasttext.parar_treinamento()
        return HttpResponse(texto='Treinamento parado.', status=HTTPStatus.OK)
    except Exception as erro:
        return HTTPException(detail='Ocorreu um erro ao tentar parar o treinamento', status_code=500)

@app.get("/treinamento/obter-status-treinamento")
async def obter_status_treinamento():
    treinamento = Treinamento()
    try:
        if not treinamento.estaEmTreinamento():
            treinamento.iniciarTreinamento(forceRestart=True)
            return "Treinamento iniciado"
        else:
            return "Já existe um treinamento em andamento"
    except Exception as erro:
        return HTTPException(detail='Ocorreu um erro ao tentar obter o status do treinamento', status_code=500)


@app.post("/medicamentos/importar-csv-medicamentos")
async def importar_csv_medicamentos(csv_file: UploadFile = File(...)):
    try:
        if csv_file is None:
            raise HTTPException(status_code=400, detail="Arquivo CSV não foi enviado.")
        
        servico_medicamentos = MedicamentosServico()
        file_content = await csv_file.read()

        await servico_medicamentos.preencher_tabelas_medicamentos(file_content)
        await inicia_pre_processamento()

        return {"texto": 'Arquivo importado com sucesso'}
    except Exception as erro:
        print(f"Erro: {erro}")
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar importar o CSV de medicamentos')


@app.post("/suprimentos/importar-csv-suprimentos")
async def importar_csv_suprimentos(csvFile: UploadFile = File(None)):
    try:
        servico_suprimentos = SuprimentosServico()
        await servico_suprimentos.inserir_suprimentos(csvFile)
        #await inicia_pre_processamento()
        return {"texto": 'Arquivo importado com sucesso'}
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar importar o CSV de medicamentos')
    
@app.get("/medicamentos/consultar-grupo")
async def consultar_grupo(
    busca: str = Query(..., description="Termo de busca"),
    offset: int = Query(0, description="Deslocamento para paginação"),
    limit: int = Query(10, description="Limite de resultados por página")
):
    try:
        servico_medicamentos = MedicamentosServico()
        medicamentos = servico_medicamentos.consultar_transacoes_pela_descricao(busca, offset, limit)
        """ 
        Se o fasttext estiver ok, descomente o trecho abaixo
        modelo = fasttext.load_model("_model/model.bin")
        label = model.predict_proba([busca],k=1)[0][0][0]
        medicamentos_filtrados = servico_medicamentos.obter_medicametos_pela_label(label, offset, limit)
        medicamentos = medicamentos + medicamentos_filtrados[0:100]
        """
        
        return { 'medicamentos': medicamentos }
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar consultar o grupo de medicamentos')
    
@app.get("/medicamentos/consultar-clean")
async def consultar_clean(
    busca: str = Query(..., description="Termo de busca"),
    offset: int = Query(0, description="Deslocamento para paginação"),
    limit: int = Query(10, description="Limite de resultados por página")
):
    try:
        servico_medicamentos = MedicamentosServico()
        medicamentos = servico_medicamentos.consultar_transacoes_pelo_clean(busca, offset, limit)
        return { 'medicamentos': medicamentos }
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar consultar o clean dos medicamentos')
    
@app.get("/suprimentos/descricao")
async def consultar_descricao(
    busca: str = Query(..., description="Termo de busca"),
    offset: int = Query(0, description="Deslocamento para paginação"),
    limit: int = Query(10, description="Limite de resultados por página")
):
    try:
        servico_suprimentos = SuprimentosServico()
        suprimentos = servico_suprimentos.consultar_pela_descricao(busca, offset, limit)
        return { 'suprimentos': suprimentos }
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar consultar a descrição dos medicamentos')

@app.get("/obter-colunas")
def consultar_colunas():
    try:
        return {
            'medicamentos':  ['Clean','Descricao', 'Grupo', 'Quantidade', 'Valor Unitário'],
            'suprimentos': ['UF', 'Nome', 'Ano', 'Descrição', 'Quantidade', 'Valor Unitário', 'Valor Total']
        }
    except Exception as erro:
        raise HTTPException(status_code=500, detail='Ocorreu um erro ao tentar obter as colunas')
    


app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)