from repositorios.medicamentos_repositorio import MedicamentosRepositorio
import pandas as pd
import random
import io

class MedicamentosServico():
    def __init__(self):
        self.repositorio = MedicamentosRepositorio()
        
    async def preencher_tabelas_medicamentos(self, csv_file):
        try:
            self.__inserir_transacoes(csv_file)
            self.__inserir_produtos()
            self.__inserir_produtos_transacoes()
            self.__inserir_classes()
            self.__inserir_produtos_classes()
            
            return { "text": 'Tabelas preenchidas com sucesso!', "erro": False }
        except Exception as erro:
            raise erro
    
    def __inserir_transacoes(self, csv_file): 
        try:
            # Converter os bytes em um objeto de buffer de bytes
            if isinstance(csv_file, bytes):
                csv_file = io.BytesIO(csv_file)
            
            cols = [
                "CodigoNFe", 
                "DataEmissao", 
                "MunicipioEmitente", 
                "unidadecomercial", 
                "quantidadecomercial", 
                "valorunitariocomercial", 
                "DescricaoProduto", 
                "CLEAN"
            ]
            df = pd.read_csv(csv_file, usecols=cols, dtype={
                "CodigoNFe": int,
                "DataEmissao": str,
                "MunicipioEmitente": str,
                "unidadecomercial": str,
                "quantidadecomercial": float,
                "valorunitariocomercial": float,
                "DescricaoProduto": str,
                "CLEAN": str
            }, sep=',')
            
            df = df.applymap(lambda x: x.replace('\'', '') if isinstance(x, str) else x)
            input_array = df.to_records(index=False).tolist()
            
            self.repositorio.inserir_transacoes(input_array)
        except Exception as erro:
            print(f"ERROR :: MedicamentosService :: __inserir_transacoes :: {erro}")
            raise erro
        
    def __obter_transacoes_unicas(self):
        return self.repositorio.obter_transacoes_unicas()
    
    def __inserir_produtos(self):
        produtos_a_inserir = []
        
        for transacao in self.__obter_transacoes_unicas():
            transacao = list(transacao)
            transacao[0] = transacao[0].replace('\'', '')
            transacao[1] = transacao[1].replace('\'', '')
            transacao = tuple(transacao)
            produtos_a_inserir.append((transacao[0], transacao[1]))
            
        if produtos_a_inserir:
            self.repositorio.inserir_produtos(produtos_a_inserir)
        
    def __inserir_produtos_transacoes(self):
        transacoes_com_produtos = self.repositorio.obter_transacoes_com_produtos()
        transacoes_produtos = [(transacao[0], transacao[1]) for transacao in transacoes_com_produtos]
        self.repositorio.inserir_transacoes_produtos(transacoes_produtos)
        
    def __inserir_classes(self):
        try:
            with open('classes.txt', 'r') as f:
                classes = f.read().strip().split(',')
            if not classes:
                return
            classes = [(cls.replace('\'', '').replace('(', '').replace(')', ''),) for cls in classes]
            self.repositorio.inserir_classes(classes)
        except Exception as erro:
            raise erro
        
    def __inserir_produtos_classes(self):
        try:
            maximo_classes = self.repositorio.obter_max_classes()
            maximo_classes = maximo_classes[0]
            minimo_classes = self.repositorio.obter_min_classes()
            minimo_classes = minimo_classes[0]
            produtos = self.repositorio.obter_id_produtos()
            
            input_products_classes_array = []
            for produto_id in produtos:
                produto_id = produto_id[0]
                input_products_classes_array.append((produto_id, random.randint(minimo_classes[0], maximo_classes[0]), 'training'))
            
            self.repositorio.inserir_produtos_classes(input_products_classes_array)
        except Exception as erro:
            raise erro
           
    def consultar_transacoes_pela_descricao(self, busca: str, offset: int, limit: int):
        transacoes_db = self.repositorio.consultar_transacoes_pela_descricao(busca, offset, limit)

        if not transacoes_db:
            print("Nenhuma transação encontrada.")
            return []

        transacoes = [
            [
                transacao[0],
                transacao[1],
                transacao[2],
                transacao[3],
                transacao[4],
            ]
            for transacao in transacoes_db            
        ]
        return transacoes

    def obter_medicamentos_pela_label(self, label, offset, limit):
        medicamentos_db = self.repositorio.consultar_medicametos_pela_label(label, offset, limit)
        
        medicamentos = [
            {
                'id': medicamento[0],
                'CodigoNFe': medicamento[1],
                'DataEmissao': medicamento[2],
                'MunicipioEmitente': medicamento[3],
                'unidadecomercial': medicamento[4],
                'quantidadecomercial': medicamento[5],
                'valorunitariocomercial': medicamento[6],
                'DescricaoProduto': medicamento[7],
                'CLEAN': medicamento[8]
            }
            for medicamento in medicamentos_db
        ]
            
        return medicamentos
    
    def consultar_transacoes_pelo_clean(self, busca: str, offset: int, limit):
        medicamentos_db = self.repositorio.consultar_medicamentos_pelo_clean(clean=busca, offset=offset, limit=limit)
        
        medicamentos = [
            [
                medicamento[0],
                medicamento[1],
                medicamento[2],
                medicamento[3],
                medicamento[4],
            ]
            for medicamento in medicamentos_db
        ]
        
        return medicamentos