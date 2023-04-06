from _data_augmentation import data_augmentation
from _data_augmentation.Args import Args


def run():
    data_augmentation.run(Args(
        src_file="../datasets/medicamentos/medicamentos.csv",
        target_file="../datasets/medicamentos/medicamentos_aumentado.csv",
        dataset_name="medicamentos",
        request_delay=2
    ))
    # os.system('cmd /c "python ../_data_augmentation/data_augmentation.py \"../datasets/medicamentos/medicamentos.csv\" \"../datasets/medicamentos/medicamentos_aumentado.csv\" medicamentos 5"')