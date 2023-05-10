from _pre_processamento.controleDeTreinamento import ControleDeTreinamento
from . import medicamentos_augmentation
from . import anvisa_prod_augmentation
from . import anvisa_pa_augmentation
import _log_debug.logger as logger

def run():
    if ControleDeTreinamento.running:
        if ("init_data_augmentation iniciado" in logger.lastLine()) or ("init_data_augmentation --> medicamentos_augmentation iniciado" in logger.lastLine()):
            logger.log("init_data_augmentation --> medicamentos_augmentation iniciado")
            medicamentos_augmentation.run()
            if ControleDeTreinamento.running:
                logger.log("init_data_augmentation --> medicamentos_augmentation finalizado")

    if ControleDeTreinamento.running:
        if ("init_data_augmentation --> medicamentos_augmentation finalizado" in logger.lastLine()) or ("init_data_augmentation --> anvisa_prod_augmentation iniciado" in logger.lastLine()):
            logger.log("init_data_augmentation --> anvisa_prod_augmentation iniciado")
            anvisa_prod_augmentation.run()
            if ControleDeTreinamento.running:
                logger.log("init_data_augmentation --> anvisa_prod_augmentation finalizado")

    if ControleDeTreinamento.running:
        if ("init_data_augmentation --> anvisa_prod_augmentation finalizado" in logger.lastLine()) or ("init_data_augmentation --> anvisa_pa_augmentation iniciado" in logger.lastLine()):
            logger.log("init_data_augmentation --> anvisa_pa_augmentation iniciado")
            anvisa_pa_augmentation.run()
            if ControleDeTreinamento.running:
                logger.log("init_data_augmentation --> anvisa_pa_augmentation finalizado")


# run()