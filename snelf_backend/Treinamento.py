import os
import sys
import threading
import time

from _model import treinar_modelo
from _model.treinar_modelo import pararTreinamentoModelo
from _pre_processamento import init_pre_processamento
from _pre_processamento.controleDeTreinamento import ControleDeTreinamento


class Treinamento:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)

        return cls._self

    def pararTreinamento(self):
        self._pararInstanciasTreinamentoThread()
        pararTreinamentoModelo()

    def iniciarTreinamento(self, forceRestart = False):
        minha_thread = _ThreadTreinamento()
        minha_thread.forceRestart = forceRestart
        minha_thread.start()

    def estaEmTreinamento(self) -> bool:
        return len(_ThreadTreinamento.instancias_ativas) > 0

    def obterStatusTreinamento(self) -> str:
        status = "O modelo não está treinado."

        running = "[RUNNING] " if self.estaEmTreinamento() else "[STOPPED] "

        statusPreProcessamento = self._obterStatusPreProcessamento()
        if statusPreProcessamento is not None:
            status = running + statusPreProcessamento

            if 'train_test_split finalizado' in statusPreProcessamento:
                statusTreinamentoModelo = self._obterStatusTreinamentoModelo()
                if statusTreinamentoModelo is not None:
                    status = running + statusTreinamentoModelo

        return status


    def _obterStatusPreProcessamento(self):
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

    def _obterStatusTreinamentoModelo(self):
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

    def _pararInstanciasTreinamentoThread(self):
        ControleDeTreinamento.running = False
        while len(_ThreadTreinamento.instancias_ativas) > 0:
            continue

class _ThreadTreinamento(threading.Thread):
    instancias_ativas = []
    forceRestart = False
    def __init__(self):
        super().__init__()
        _ThreadTreinamento.instancias_ativas.append(self)

    def run(self):
        try:
            localDir = str(os.path.dirname(os.path.abspath(__file__)))
            ControleDeTreinamento.running = True
            init_pre_processamento.run(self.forceRestart)
            if ControleDeTreinamento.running:
                treinar_modelo.run(localDir)
            _ThreadTreinamento.instancias_ativas.remove(self)
        except Exception as ex:
            treinamento = Treinamento()
            treinamento.pararTreinamento()
            raise ex