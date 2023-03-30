import os

def run():
    os.system('cmd /c "python ../_data_augmentation/data_augmentation.py \"../datasets/medicamentos/medicamentos.csv\" \"../datasets/medicamentos/medicamentos_aumentado.csv\" medicamentos 5"')