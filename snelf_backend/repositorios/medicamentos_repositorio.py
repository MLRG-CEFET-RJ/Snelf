from dao.medicamentos_dao import MedicamentosDAO

class MedicamentosRepositorio:
    def __init__(self):
        self.dao = MedicamentosDAO()

    def iniciar_transacao(self):
        self.dao.iniciar_transacao()

    def commit_transacao(self):
        self.dao.commit_transacao()
    
    def rollback_transacao(self):
        self.dao.rollback_transacao()

    def obter_transacoes_unicas(self):
        return self.dao.selecionar_transacoes_unicas()

    def inserir_produtos(self, produtos):
        self.dao.inserir_produtos(produtos)
        
    def obter_transacoes_com_produtos(self):
        return self.dao.obter_transacoes_com_produtos()
    
    def inserir_transacoes_produtos(self, transacoes_produtos):
        self.dao.inserir_transacoes_produtos(transacoes_produtos)
        
    def inserir_classes(self, classes):
        self.dao.inserir_classes(classes)
        
    def obter_max_classes(self):
        return self.dao.obter_max_classes()
    
    def obter_min_classes(self):
        return self.dao.obter_min_classes()
    
    def obter_id_produtos(self):
        return self.dao.obter_ids_produtos()
    
    def inserir_produtos_classes(self, produtos_classes_array):
        return self.dao.inserir_produtos_classes(produtos_classes_array)
    
    def inserir_transacoes(self, transacoes):
        return self.dao.inserir_transacoes(transacoes)
    
    def consultar_medicametos_pela_label(self, label, offset, limit):
        return self.dao.consultar_medicamentos_pela_label(label, offset, limit)
    
    def consultar_medicamentos_pelo_tipo_de_busca(self, filters, offset, limit):
        return self.dao.consultar_medicamentos_pelo_tipo_de_busca(filters, offset, limit)
    
    def total_registros(self):
        return self.dao.total_registros();
