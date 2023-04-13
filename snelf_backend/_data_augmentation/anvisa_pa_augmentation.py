from _data_augmentation import data_augmentation
from _data_augmentation.Args import Args


def run():
    data_augmentation.run(Args(
        src_file="datasets/anvisa/anvisa.csv",
        target_file="datasets/anvisa/anvisa_principio_ativo_aumentado.csv",
        dataset_name="anvisa",
        request_delay=5,
        use_col="principio_ativo"
    ))

    # os.system('cmd /c "python ../_data_augmentation/data_augmentation.py \"../datasets/anvisa/anvisa.csv\" \"../datasets/anvisa/anvisa_principio_ativo_aumentado.csv\" anvisa 5 --use_col principio_ativo"')