from treinamento import Treinamento

class ManipuladorFasttext():
    def __init__(self):
        self.treinamento = Treinamento()
        
    def iniciar_treinamento(self):
        try:
            if self.treinamento.estaEmTreinamento():
                return {
                    "texto": 'Já existe um treinamento em andamento', 
                    "status": 200,
                    "erro": False
                }
            self.treinamento.iniciarTreinamento(forceRestart=True)
            return {
                    "texto": 'Treinamento iniciado', 
                    "status": 200,
                    "erro": False
            }
        except Exception as erro:
            return {
                    "texto": 'Treinamento iniciado', 
                    "status": 422,
                    "erro": True,
                    "erro_info": erro
            }
            
    def obter_status_treinamento(self):
        try:
            return self.treinamento.obterStatusTreinamento()
        except Exception as erro:
            return {
                    "texto": 'Ocorreu um erro ao tentar obter o status do treinamento', 
                    "status": 500,
                    "erro": True,
                    "erro_info": erro
            }