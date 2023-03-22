from . import medicamentos_augmentation
from . import anvisa_prod_augmentation
from . import anvisa_pa_augmentation

def run():
    medicamentos_augmentation.run()
    anvisa_prod_augmentation.run()
    anvisa_pa_augmentation.run()


# run()