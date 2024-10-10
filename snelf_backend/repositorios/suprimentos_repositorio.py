from dao.suprimentos_dao import SuprimentosDao

class SuprimentosRepositorio():
    def __init__(self):
        self.dao = SuprimentosDao()
        
    def inserir_suprimentos(self, suprimentos):
        return self.dao.inserir_suprimentos(suprimentos)
    def consultar_pela_descricao(self, busca, offset, limit):
        return self.dao.consultar_pela_descricao(busca, offset, limit)