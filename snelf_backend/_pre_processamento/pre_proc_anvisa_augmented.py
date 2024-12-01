# original_words = None

def run():
    # -*- coding: utf-8 -*-
    """pre_proc_anvisa_augmented.ipynb

    Automatically generated by Colaboratory.

    Original file is located at
        https://colab.research.google.com/drive/1U5CBFmTuVayaau1cDsA39rgYg6W_USka
    """

    import sys
    sys.path.append('..')

    """## Exemplo de uso da lib Extractor"""

    from _libs.extractor import Extractor as xtc

    descricao = 'OXALIPLATINA 50 MG PÓ LIOFILIZADO FR/AMP X 500 MG'
    xtc.extract(descricao)

    """## Config

    ### Imports
    """

    import pandas as pd
    import re
    import nltk
    # nltk.download('stopwords')
    # nltk.download('punkt')
    
    nltk.download('punkt_tab')

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from string import punctuation

    from _libs.extractor import Extractor as xtc

    pd.set_option('display.max_colwidth', None)

    """### Stopwords"""

    # loading new_stopwords
    with open('_pre_processamento/custom_stopwords.txt') as f:
        data = f.read()
    new_stopwords = data.split()

    # updating stopwords with new_stopwords
    stopwords = set(stopwords.words('portuguese') + list(punctuation))
    print(len(stopwords))

    custom_stopwords = stopwords.copy()
    custom_stopwords.update(new_stopwords)
    print(len(custom_stopwords))

    """### Functions"""

    def clean_desc(words, desc):
        subs = [sub.strip() for sub in re.split('‹|–|::|-|\|', desc)]  # split in substrings
        new_desc = ''

        for sub in subs:
            for word in words:
                if word in sub.split():
                    new_desc += ' {}'.format(sub)
                    break

        return new_desc.strip()  # return without extra initial space

    def get_words(text):
        return [w for w in word_tokenize(text) if w.lower() not in custom_stopwords]

    def remove_separator(terms):
        return [re.sub('\s|/', '', t) if t is not None else t for t in terms]

    # clean_desc Example
    desc = 'GLICOSE 5% CX C/40 FRASCOS X 250ML'
    deriv = 'SORO DE GLICOSE 5% - EUROFARMA | DENTAL CREMER PRODUTOS'

    print(desc)
    print(clean_desc(get_words(desc), deriv))

    # Extractor example
    produto = 'ESPIRONOLACTONA 100MG CX C/30 CP'
    principio_ativo, concentracao, forma_farmaceutica, quantidade = xtc.extract(produto)

    print(' ---- '.join([principio_ativo, concentracao, forma_farmaceutica, quantidade]))

    """### Path"""

    data_path = 'datasets/anvisa/augmented/'
    data_prod = 'anvisa_produto_aumentado.csv'
    data_pa = 'anvisa_principio_ativo_aumentado.csv'

    """## Parse

    ### Removendo ";" que não representa o separador do CSV
    """

    def custom_replace(desc):
        start = desc.find(';') + 1
        end = desc.rfind(';')
        return desc[:start] + desc[start:end].replace(';', ',') + desc[end:]

    def fix_csv(src, target):
        buff = 300
        content = ''

        with open(src, 'r', encoding='utf-8') as fs:
            with open(target, 'w', encoding='utf-8') as ft:
                ft.write(fs.readline())  # header
                lines = fs.readlines(buff)
                while lines:
                    for line in lines:
                        content += custom_replace(line)
                    ft.write(content)
                    content = ''
                    lines = fs.readlines(buff)

    # produto
    src_file = '{}{}'.format(data_path, data_prod)
    target_file = '{}{}_mod.csv'.format(data_path, data_prod[:-4])
    fix_csv(src_file, target_file)

    # principio_ativo
    src_file = '{}{}'.format(data_path, data_pa)
    target_file = '{}{}_mod.csv'.format(data_path, data_pa[:-4])
    fix_csv(src_file, target_file)

    """## Pré-processamento PRODUTO

    ### Loading
    """

    # header => ['cod', 'descricao', 'ean']
    data_file = 'anvisa_produto_aumentado_mod.csv'
    src = '{}{}'.format(data_path, data_file)

    df = pd.read_csv(src, dtype={0: int, 1: str, 2: str}, sep=';', encoding='utf-8')
    df.shape

    """### Removendo substrings com base nas palavras da descrição original

    ### Removendo registros com base nos termos principais
    """

    idxs = list()
    removed = list()

    # iterate over dataframe
    for index, row in df.iterrows():
        if row['cod'] == 2:
            original_words = get_words(row['descricao'])  # get non stopwords
            _, conc, _, qtd = xtc.extract(row['descricao'])  # get principal terms
            conc, qtd = remove_separator([conc, qtd])
            master_idx = index
            continue

        new_desc = clean_desc(original_words, row['descricao'])  # remove irrelevant substrings
        if not new_desc:
            idxs.append(index)  # storage index for future drop
            removed.append([master_idx, index])
            continue

        _, new_conc, _, new_qtd = xtc.extract(new_desc)  # get principal terms
        new_conc, new_qtd = remove_separator([new_conc, new_qtd])

        if conc == new_conc and qtd == new_qtd:
            df.at[index, 'descricao'] = new_desc  # replace descricao with cleaned new_desc
        else:
            idxs.append(index)  # storage index for future drop
            removed.append([master_idx, index])

    """### Removed"""

    df_removed = pd.DataFrame(removed, columns=['master_idx', 'removed_idx'])
    df_removed.head()

    df_grouped = df_removed.groupby('master_idx')['removed_idx'].apply(list).reset_index()
    df_grouped.head()

    # master, removed = df_grouped.loc[3002].values
    # indexes = [master] + removed
    # df.loc[indexes][['cod', 'descricao']]

    # DEBUG

    descricao = 'NIMESULIDA 100 MG COM CT BL AL PLAS INC X 12'
    derivado = 'NIMESULIDA GEOLAB 100MG, CAIXA COM 12 COMPRIMIDOS | CR PRO'

    original_words = get_words(descricao)  # get non stopwords
    _, conc, _, qtd = xtc.extract(descricao)  # get principal terms
    conc, qtd = remove_separator([conc, qtd])
    print(original_words)
    print(conc, qtd, '\n')

    new_desc = clean_desc(original_words, derivado)  # remove irrelevant substrings
    _, new_conc, _, new_qtd = xtc.extract(new_desc)  # get principal terms
    new_conc, new_qtd = remove_separator([new_conc, new_qtd])
    print(new_desc)
    print(new_conc, new_qtd, '\n')

    if conc == new_conc and qtd == new_qtd:
        print('igual')

    """### Removing"""

    df.drop(idxs, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.shape

    """#### Removendo registros  com os termos
    * BULA
    * PREÇO
    * BARATO
    """

    cond1 = df['cod'] == 2
    # or (
    cond2 = df['cod'] == 4
    # and
    cond3 = ~df['descricao'].str.contains('BULA|PREÇO|BARATO', regex=True)
    # )

    df = df[cond1 | (cond2 & cond3)]
    df.shape

    """#### Removendo os termos <font color='red'>(devem ser removidos nesta ordem)</font>
    * EM MERCADO LIVRE BRASIL
    * EM MERCADO LIVRE
    * NO MERCADO LIVRE BRASIL
    * NO MERCADO LIVRE
    * COMPRAR EM ILHA DENTAL
    * COMPRAR EM AGROFORTE
    * COMPRAR EM FARMA PRATA
    * ONDE COMPRAR (apenas no início do registro)
    * COMPRAR
    * ENCONTRE (apenas no início do registro)

    #### Após as remoções acima, remover os registros com os termos
    * ENCONTRE
    """

    pattern1 = r'(?i)(em|no)?\s+mercado\s+livre\s*(brasil)?'
    pattern2 = r'(?i)comprar em (ilha dental|agroforte|farma prata)'
    pattern3 = r'(?i)(onde)?\s*comprar'
    pattern4 = r'(?i)^encontre'

    replaces = {pattern1: '',
                pattern2: '',
                pattern3: '',
                pattern4: '', }

    df.replace(replaces, regex=True, inplace=True)

    cond1 = df['cod'] == 2
    cond2 = ~df['descricao'].str.contains('ENCONTRE')
    df = df[cond1 | cond2]
    df.shape

    pattern = r'(?i)mercado livre|comprar|encontre'
    df[df['descricao'].str.contains(pattern)]

    pattern = r'(?i)oferta'
    df[df['descricao'].str.contains(pattern)].shape

    df.head()

    # after removing, strip again
    df['descricao'] = df['descricao'].str.strip()

    start = 5000
    end = start + 20
    cod = df['cod'].tolist()[start:end]
    desc = df['descricao'].tolist()[start:end]
    lista = list(zip(cod, desc))
    for cod, desc in lista:
        if cod == 4:
            tab = '\t'
            br = ''
        else:
            tab = ''
            br = '\n'
            original_words = [w for w in desc if len(w) > 2]
        print('{}{}{}'.format(br, tab, desc))

    """### Gravando em arquivo"""

    data_prod = 'anvisa_produto_aumentado_preproc.csv'
    df.to_csv('{}{}'.format(data_path, data_prod),
              sep=';',
              header=df.columns,
              index=False,
              encoding='utf-8')

    """## Pré-processamento PRINCÍPIO ATIVO

    ### Loading
    """

    # header => ['cod', 'descricao', 'ean']
    data_pa = 'anvisa_principio_ativo_aumentado_mod.csv'
    src = '{}{}'.format(data_path, data_pa)

    df = pd.read_csv(src, dtype={0: int, 1: str, 2: str}, sep=';')
    df.shape

    """### Removendo substrings com base nas palavras da descrição original

    ### Removendo registros com base nos termos principais
    """

    idxs = list()
    removed = list()

    # iterate over dataframe
    for index, row in df.iterrows():
        if row['cod'] == 2:
            original_words = get_words(row['descricao'])  # get non stopwords
            _, conc, _, qtd = xtc.extract(row['descricao'])  # get principal terms
            conc, qtd = remove_separator([conc, qtd])
            master_idx = index
            continue

        new_desc = clean_desc(original_words, row['descricao'])  # remove irrelevant substrings
        if not new_desc:
            idxs.append(index)  # storage index for future drop
            removed.append([master_idx, index])
            continue

        _, new_conc, _, new_qtd = xtc.extract(new_desc)  # get principal terms
        new_conc, new_qtd = remove_separator([new_conc, new_qtd])

        if conc == new_conc and qtd == new_qtd:
            df.at[index, 'descricao'] = new_desc  # replace descricao with cleaned new_desc
        else:
            idxs.append(index)  # storage index for future drop
            removed.append([master_idx, index])

    """### Removing"""

    df.drop(idxs, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.shape

    """#### Removendo registros  com os termos
    * BULA
    * PREÇO
    * BARATO
    """

    cond1 = df['cod'] == 2
    # or (
    cond2 = df['cod'] == 4
    # and
    cond3 = ~df['descricao'].str.contains('BULA|PREÇO|BARATO', regex=True)
    # )

    df = df[cond1 | (cond2 & cond3)]
    df.shape

    """#### Removendo os termos <font color='red'>(devem ser removidos nesta ordem)</font>
    * EM MERCADO LIVRE BRASIL
    * EM MERCADO LIVRE
    * NO MERCADO LIVRE BRASIL
    * NO MERCADO LIVRE
    * COMPRAR EM ILHA DENTAL
    * COMPRAR EM AGROFORTE
    * COMPRAR EM FARMA PRATA
    * ONDE COMPRAR (apenas no início do registro)
    * COMPRAR
    * ENCONTRE (apenas no início do registro)

    #### Após as remoções acima, remover os registros com os termos
    * ENCONTRE
    """

    pattern1 = r'(?i)(em|no)?\s+mercado\s+livre\s*(brasil)?'
    pattern2 = r'(?i)comprar em (ilha dental|agroforte|farma prata)'
    pattern3 = r'(?i)(onde)?\s*comprar'
    pattern4 = r'(?i)^encontre'

    replaces = {pattern1: '',
                pattern2: '',
                pattern3: '',
                pattern4: '', }

    df.replace(replaces, regex=True, inplace=True)

    cond1 = df['cod'] == 2
    cond2 = ~df['descricao'].str.contains('ENCONTRE')
    df = df[cond1 | cond2]
    df.shape

    # after removing, strip again
    df['descricao'] = df['descricao'].str.strip()

    """### Gravando em arquivo"""

    data_pa = 'anvisa_principio_ativo_aumentado_preproc.csv'
    df.to_csv('{}{}'.format(data_path, data_pa),
              sep=';',
              header=df.columns,
              index=False,
              encoding='utf-8')