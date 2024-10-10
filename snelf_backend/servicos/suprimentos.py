from repositorios.suprimentos_repositorio import SuprimentosRepositorio
import os
import pandas as pd

class SuprimentosServico():
    def __init__(self):
        self.repositorio = SuprimentosRepositorio()
        
    def inserir_suprimentos(self, csvFile):
        try:
            csv = os.path.join(os.getcwd(), 'suprimentos_impressora.csv')
            if csvFile: 
                csv = csvFile.file
            cols = ["Ano Licitação", "UF", "Nome UASG", "Descrição", "Quantidade", "Valor Unitário Homologado", "Valor Total Homologado"]
            df = pd.read_csv(csv, usecols=cols, dtype={
                "Ano Licitação": str,
                "UF": str,
                "Nome UASG": str,
                "Descrição": str,
                "Quantidade": str,
                "Valor Unitário Homologado": str,
                "Valor Total Homologado": str,
            }, sep=',')
            
            df = df.applymap(lambda x: x.replace('\'', '') if isinstance(x, str) else x)
            
            inputArray = df.to_records(index=False).tolist()
            
            return self.repositorio.inserir_suprimentos(inputArray)
        except Exception as erro:
            raise erro
        
    def consultar_pela_descricao(self, busca, offset, limit):
        try:
            return self.repositorio.consultar_pela_descricao(busca, offset, limit)
        except Exception as erro:
            raise erro