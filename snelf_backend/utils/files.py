import pandas as pd
import numpy as np

class ManipuladorDeArquivos():
    def escrever_dados_treinamento_txt (self, csv_file, path='./dados/data.train.txt'):
        data_frame = pd.read_csv(csv_file, sep=';')
        np.savetxt(path, data_frame, fmt='%s')