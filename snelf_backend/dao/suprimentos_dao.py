from dao.base_dao import BaseDAO

class SuprimentosDao(BaseDAO):
    def __init__(self):
        super().__init__()
        
    def inserir_suprimentos(self, suprimentos):
        query_base = "INSERT INTO suprimentos (uf, nomeuasg, ano, descricao, quantidade, valor_unitario_homologado, valor_total_homologado) VALUES "
        query_valores = ", ".join(["(%s, %s, %s, %s, %s, %s, %s)"] * len(suprimentos))
        query = query_base + query_valores
        valores = [item for sublista in suprimentos for item in sublista]
        return self.insert(query, valores)
    
    def consultar_pela_descricao(self, busca, offset, limit):
        query = f""" SELECT uf, 
                            nomeuasg, 
                            ano, 
                            descricao, 
                            quantidade, 
                            valor_unitario_homologado, 
                            valor_total_homologado
                    FROM suprimentos 
                    WHERE LOWER(descricao) LIKE LOWER('%{busca}%')
                    LIMIT {limit}
                    OFFSET {offset}
                """
        return self.select(query)