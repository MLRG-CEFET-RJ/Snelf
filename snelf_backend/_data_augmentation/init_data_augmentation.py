from . import medicamentos_augmentation
from . import anvisa_prod_augmentation
from . import anvisa_pa_augmentation
import _log_debug.logger as logger

def run():
    logger.log("init_data_augmentation --> medicamentos_augmentation iniciado")
    medicamentos_augmentation.run()
    logger.log("init_data_augmentation --> medicamentos_augmentation finalizado")
    logger.log("init_data_augmentation --> anvisa_prod_augmentation iniciado")
    anvisa_prod_augmentation.run()
    logger.log("init_data_augmentation --> anvisa_prod_augmentation finalizado")
    logger.log("init_data_augmentation --> anvisa_pa_augmentation iniciado")
    anvisa_pa_augmentation.run()
    logger.log("init_data_augmentation --> anvisa_pa_augmentation finalizado")


# run()