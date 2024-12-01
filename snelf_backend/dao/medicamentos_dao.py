from dao.base_dao import BaseDAO

class MedicamentosDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        
    def iniciar_transacao(self):
        return self.iniciar_transacao_db()

    def commit_transacao(self):
        return self.commit_transacao_db()

    def rollback_transacao(self):
        return self.rollback_transacao_db()
        
    def selecionar_transacoes_unicas(self):
        query = "SELECT DISTINCT descricaoproduto, clean FROM transactions"
        return self.select(query)

    def inserir_produtos(self, produtos):
        query_base = "INSERT INTO produtos (description, clean) VALUES "
        query_valores = ", ".join(["(%s, %s)"] * len(produtos))
        query = query_base + query_valores
        valores = [item for sublista in produtos for item in sublista]
        self.insert(query, valores)
        
    def obter_transacoes_com_produtos(self):
        query = """
            SELECT DISTINCT p.id AS id_produto, t.id AS id_transacao
            FROM transactions t 
            JOIN produtos p ON p.description = t.descricaoproduto
        """
        return self.select(query)
    
    def inserir_transacoes_produtos(self, transacoes_produtos):
        query_base = "INSERT INTO products_transactions(id_product, id_transaction) VALUES "
        query_valores = ", ".join(["(%s, %s)"] * len(transacoes_produtos))
        query = query_base + query_valores
        valores = [item for sublista in transacoes_produtos for item in sublista]
        return self.insert(query, valores)
    
    def inserir_classes(self, classes):
        query_base = "INSERT INTO classes (class_label) VALUES "
        query_valores = ", ".join(["(%s)"] * len(classes))
        query = query_base + query_valores
        valores = [item for sublista in classes for item in sublista]
        return self.insert(query, valores)
    
    def obter_max_classes(self):
        query = "SELECT MAX(id) FROM classes"
        return self.select(query)
    
    def obter_min_classes(self):
        query = "SELECT MIN(id) FROM classes"
        return self.select(query)
    
    def obter_ids_produtos(self):
        query = "SELECT id FROM produtos"
        return self.select(query)
    
    def  inserir_produtos_classes(self, produtos_classes_array):
        query_base = "INSERT INTO products_classes(id_produto, id_classe, association_type) VALUES "
        query_valores = ", ".join(["(%s, %s, %s)"] * len(produtos_classes_array))
        query = query_base + query_valores
        valores = [item for sublista in produtos_classes_array for item in sublista]
        return self.insert(query, valores)
    
    def inserir_transacoes(self, transacoes):
        query_base = "INSERT INTO transactions(CodigoNFe,DataEmissao,MunicipioEmitente,unidadecomercial,quantidadecomercial,valorunitariocomercial,DescricaoProduto,CLEAN) VALUES "
        query_valores = ", ".join(["(%s, %s, %s, %s, %s, %s, %s, %s)"] * len(transacoes))
        query = query_base + query_valores
        valores = [item for sublista in transacoes for item in sublista]
        return self.insert(query, valores)

    def consultar_medicamentos_pela_label(self, label, offset, limit):
        query = f"""SELECT t.*
                    FROM products_classes pc
                    JOIN classes c 
                        on c.id=pc.id_classe
                        and c.class_label like '%{label}%'
                    JOIN products_transactions pt 
                        on pt.id_product=pc.id_produto
                    JOIN transactions t
                        on t.id=pt.id_transaction
                    LIMIT {limit}
                    OFFSET {offset}"""
        return self.select(query)
    
    def consultar_medicamentos_pelo_tipo_de_busca(self, filters, offset, limit):
        column_mapping = {
            "clean": "clean",
            "descricaoProduto": "descricaoproduto",
            "unidadeComercial": "unidadecomercial",
            "valorUnitarioComercial": "valorunitariocomercial"
        }

        conditions = []
        
        for attr, column in column_mapping.items():
            filter_value = getattr(filters, attr, None)
            if filter_value:
                if isinstance(filter_value, str):
                    conditions.append(f"LOWER(t.{column}) LIKE LOWER(:{attr})")
                else:
                    conditions.append(f"t.{column} = :{attr}")
        
        condition_str = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
            SELECT 
                clean, 
                descricaoproduto, 
                unidadecomercial,
                quantidadecomercial,
                valorunitariocomercial
            FROM transactions t
            {condition_str}
            LIMIT :limit OFFSET :offset
        """

        params = {
            "clean": f"%{filters.clean}%" if filters.clean else None,
            "descricaoProduto": f"%{filters.descricaoProduto}%" if filters.descricaoProduto else None,
            "unidadeComercial": filters.unidadeComercial,
            "valorUnitarioComercial": filters.valorUnitarioComercial,
            "limit": limit,
            "offset": offset
        }
        
        params = {key: value for key, value in params.items() if value is not None}

        return self.select(query, params)

