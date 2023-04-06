from _data_augmentation import data_augmentation
from _data_augmentation.Args import Args


def run():
    data_augmentation.run(Args(
        src_file="../datasets/anvisa/anvisa.csv",
        target_file="../datasets/anvisa/anvisa_produto_aumentado.csv",
        dataset_name="anvisa",
        request_delay=5,
        use_col="produto"
    ))
    # os.system('cmd /c "python ../_data_augmentation/data_augmentation.py \"../datasets/anvisa/anvisa.csv\" \"../datasets/anvisa/anvisa_produto_aumentado.csv\" anvisa 5 --use_col produto"')