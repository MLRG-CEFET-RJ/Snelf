import pre_proc_anvisa
import pre_proc_medicamentos
from _data_augmentation import init_data_augmentation
from _move_file import move_file
import pre_proc_anvisa_augmented
import pre_proc_medicamentos_augmented
import mapeamento_ean_chave
from _oversampling import oversampling
from _training import train_test_split

def run():
    # PRE PROCESSAMENTO 1
    pre_proc_anvisa.run()
    pre_proc_medicamentos.run()

    # DATA AUGMENTATION
    init_data_augmentation.run()

    # MOVE FILES
    move_file.move("../datasets/medicamentos/medicamentos_aumentado.csv", "../datasets/medicamentos/augmented/medicamentos_aumentado.csv")
    move_file.move("../datasets/anvisa/anvisa_principio_ativo_aumentado.csv", "../datasets/anvisa/augmented/anvisa_principio_ativo_aumentado.csv")
    move_file.move("../datasets/anvisa/anvisa_produto_aumentado.csv", "../datasets/anvisa/augmented/anvisa_produto_aumentado.csv")

    # PRE PROCESSAMENTO 2
    pre_proc_anvisa_augmented.run()
    pre_proc_medicamentos_augmented.run()
    mapeamento_ean_chave.run()

    # OVERSAMPLING
    oversampling.run()

    # TRAINING
    train_test_split.run()


run()