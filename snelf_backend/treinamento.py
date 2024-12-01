import os
import threading

from _model import treinar_modelo
from _model.treinar_modelo import pararTreinamentoModelo
from _pre_processamento.controleDeTreinamento import ControleDeTreinamento


class Treinamento:
    """
    Classe singleton responsável pelo treinamento do modelo.
    """

    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)

        return cls._self

    def pararTreinamento(self):
        """
        Para o treinamento do modelo

        Utiliza a função :meth:`pararInstanciasTreinamentoThread` que para o pré-processamento

        Utiliza a função :func:`_model.treinar_modelo.pararTreinamentoModelo` que para a geração do modelo por parte do fasttext
        """

        self.pararInstanciasTreinamentoThread()
        pararTreinamentoModelo()

    def iniciarTreinamento(self, forceRestart = False):
        """
        Inicia/Retoma o treinamento do modelo.

        :param forceRestart: Indica se o treinamento deve ser reiniciado do zero (True) ou continuar de onde parou (False).
        :type forceRestart: bool
        """

        minha_thread = _ThreadTreinamento()
        minha_thread.forceRestart = forceRestart
        minha_thread.start()

    def estaEmTreinamento(self) -> bool:
        """
        Verifica se existe algum treinamento em andamento

        :return: True caso haja um treinamento em andamento. Senão retorna False
        :rtype: bool
        """
        return len(_ThreadTreinamento.instancias_ativas) > 0

    def obterStatusTreinamento(self): #-> str
        """
        Obtém o status atual do treinamento.

        Esta função:

        • Utiliza a função :meth:`estaEmTreinamento` para definir um prefixo [RUNNING] ou [STOPPED] para o treinamento

        • Utiliza a função :meth:`obterStatusPreProcessamento` para obter o status atual do pré-processamento

        • Utiliza a função :meth:`obterStatusTreinamentoModelo` para obter o status atual do treinamento do model por parte do fasttext caso seja detectado que o pré-processamento tenha terminado
        """
        status = "O modelo não está treinado."

        running = "[RUNNING] " if self.estaEmTreinamento() else "[STOPPED] "

        statusPreProcessamento = self.obterStatusPreProcessamento()
        if statusPreProcessamento is not None:
            status = running + statusPreProcessamento

            if 'train_test_split finalizado' in statusPreProcessamento: # pre processamento acabou
                statusTreinamentoModelo = self.obterStatusTreinamentoModelo()
                if statusTreinamentoModelo is not None:
                    status = running + statusTreinamentoModelo

        return status

    def obterStatusPreProcessamento(self):
        """
        Responsável por obter o status do pré-processamento.

        :return: Última linha do arquivo _log_debug/log.txt ou None
        :rtype: str or None
        """

        if os.path.exists('_log_debug/log.txt'):
            with open('_log_debug/log.txt', 'r') as f:
                linhas = f.readlines()
                if len(linhas) > 0:
                    linhas.reverse()
                    return linhas[0].strip("\n")   
                else:
                    return None
        else:
            return None

    def obterStatusTreinamentoModelo(self):
        """
        Responsável por obter o status da geração do medelo por parte do fasttext.

        :return: Última linha do arquivo _model/model.log ou None
        :rtype: str or None
        """
        if os.path.exists('_model/model.log'):
            with open('_model/model.log', 'r') as f:
                linhas = f.readlines()
                if len(linhas) > 0:
                    linhas.reverse()
                    return linhas[0].strip("\n")
                else:
                    return None
        else:
            return None

    def pararInstanciasTreinamentoThread(self):
        """
        Responsável por parar o pré-processamento

        Esta função define a variável running da classe :class:`controleDeTreinamento.ControleDeTreinamento` com o valor False
        """

        ControleDeTreinamento.running = False
        while len(_ThreadTreinamento.instancias_ativas) > 0:
            continue

class _ThreadTreinamento(threading.Thread):
    """
    Classe responsável por rodar o treinamento em uma thread separada

    Esta classe contém uma variável estática `instancias_ativas` que é uma lista de instâncias da classe :class:`treinamento._ThreadTreinamento`. sempre que uma instância da classe instâncias da classe :class:`treinamento._ThreadTreinamento` é criada essa instância é adicionada à variável estática `instancias_ativas`

    :ivar instancias_ativas: Lista de instâncias ativas da classe :class:`treinamento._ThreadTreinamento`.
    :vartype instancias_ativas: list
    """

    instancias_ativas = []

    forceRestart = False
    def __init__(self):
        super().__init__()
        _ThreadTreinamento.instancias_ativas.append(self)

    def run(self):
        """
        Quando esta função é chamada, é criada uma nova thread
        """
        try:
            localDir = str(os.path.dirname(os.path.abspath(__file__))) # fazer o projeto reconhecer o módulo em que está esse código.
            ControleDeTreinamento.running = True
            #init_pre_processamento.run(self.forceRestart)
            if ControleDeTreinamento.running:
                treinar_modelo.run(localDir)
            _ThreadTreinamento.instancias_ativas.remove(self)
        except Exception as ex:
            treinamento = Treinamento()
            treinamento.pararTreinamento()
            raise ex