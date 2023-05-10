import datetime
from _data_augmentation.Args import Args
import argparse
from _data_augmentation._log import register_log, init_log
from _data_augmentation._google import googleSearch
from _pre_processamento.controleDeTreinamento import ControleDeTreinamento


def argument_parser():
    """A method to parse up command line parameters."""

    parser = argparse.ArgumentParser()

    parser.add_argument("src_file",
                        help="Source file path. e.g. '../datasets/data.csv'")

    parser.add_argument("target_file",
                        help="Target file path. e.g. '../datasets/newdata.csv'")

    parser.add_argument("dataset_name",
                        help="One of two options: 'medicamentos' or 'anvisa'")

    parser.add_argument("request_delay",
                        type=int,
                        default=2,
                        help="Time in seconds to wait between web requests. Default is 2.")

    parser.add_argument("--use_col",
                        default='None',
                        help="In case of dataset_name is 'anvisa', one of two options: 'produto' or 'principio_ativo'")

    return parser.parse_args()


def is_subset(subset, complete_set):
    for t in subset:
        if t in complete_set:
            return True
    return False


def load_data(src_file):
    with open(src_file, 'r', encoding='utf-8') as f:
        return f.readlines()


def create_file(target_file):
    header = 'cod;descricao;ean\n'
    with open(target_file, 'w') as f:
        f.write(header)


def write_data(target_file, data):
    with open(target_file, 'a', encoding='utf-8') as f:
        f.write(''.join(data))


def extract_terms_medicamentos(extract_args):
    row, _ = extract_args

    rowPrint = str(row.encode('utf-8'))

    print("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] MEDICAMENTOS | " + rowPrint.rstrip('\n'))
    descricao, ean = row.rstrip('\n').split(';')
    termos_desc = [t for t in descricao.split() if len(t) > 2]
    return ean, descricao, termos_desc


def extract_terms_anvisa(extract_args):
    row, use_col = extract_args

    rowPrint = str(row.encode('utf-8'))

    print("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] ANVISA | " + rowPrint.rstrip('\n'))
    ean, produto, apresentacao, principio_ativo = row.rstrip('\n').split(';')
    if use_col == 'produto':
        col = produto
    elif use_col == 'principio_ativo':
        col = principio_ativo
    if col == 'NC/NI':
        descricao = None
        termos_desc = None
    else:
        descricao = ' '.join([col, apresentacao])
        termos_desc = [t for t in descricao.split() if len(t) > 2]
    return ean, descricao, termos_desc


def get_function(dataset_name):
    if dataset_name == 'medicamentos':
        return extract_terms_medicamentos
    elif dataset_name == 'anvisa':
        return extract_terms_anvisa


def proc_response(response, termos_desc, ean, s, dataset_name):
    # cod
    # 3 - derivado de um registro MEDICAMENTOS
    # 4 - derivado de um registro ANVISA
    cod = '3' if dataset_name == 'medicamentos' else '4'
    # adiciona os dados pertinentes
    for _, new_desc in response.items():
        # descarta se for um PDF
        if new_desc.startswith('[PDF]'):
            continue
        new_desc = new_desc.upper()
        termos_new = [t for t in new_desc.split() if len(t) > 2]
        # se possui pelo menos um termo da descrição original, adiciona ao conjunto
        if is_subset(termos_desc, termos_new):
            new_row = '{};{};{}\n'.format(cod, new_desc, ean)
            s.add(new_row)


def init_set(descricao, ean, dataset_name):
    # cod
    # 1 - registro original MEDICAMENTOS
    # 2 - registro original ANVISA
    cod = '1' if dataset_name == 'medicamentos' else '2'
    s = set()
    s.add('{};{};{}\n'.format(cod, descricao, ean))
    return s


def run(args: Args):

    # inicializando o log
    init_log(args.dataset_name, args.use_col)

    # carregando dados
    data = load_data(args.src_file)
    register_log('Data loaded.')

    # criando o arquivo target
    create_file(args.target_file)
    register_log('Target file created.')

    # inits
    buffer = 100
    data_augmented = list()
    extract_terms = get_function(args.dataset_name)
    register_log('Initialized variables.')

    register_log('Process started.', print_msg=True)

    data = data[1:]  # DESCARTA A PRIMEIRA LINHA POIS É CABEÇALHO
    # data = data[:1000]

    linhas_lidas = 0
    total_linhas = len(data)

    # process
    while len(data) > 0:

        if not ControleDeTreinamento.running:
            break

        dez_linhas = data[:1]

        for row in dez_linhas:

            linhas_lidas += 1

            # separa o termos
            extract_args = [row, args.use_col]
            ean, descricao, termos_desc = extract_terms(extract_args)

            if descricao is None:
                continue

            # init set
            s = init_set(descricao, ean, args.dataset_name)

            # realiza a busca no google
            response = googleSearch(descricao, delay=args.request_delay)

            # extrai os dados pertinentes
            proc_response(response, termos_desc, ean, s, args.dataset_name)

            # adiciona à lista aumentada
            for elem in sorted(s):
                data_augmented.append(elem)

            # descarrega o buffer em arquivo
            if len(data_augmented) > buffer:
                print("\n[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] BUFFER | " + str(args.target_file) + "\n")
                write_data(args.target_file, data_augmented)
                data_augmented = list()

            if linhas_lidas % 100 == 0:
                register_log('{}/{} rows processed.'.format(linhas_lidas, total_linhas))

        del data[:1]

    # descarrega o buffer residual em arquivo
    if len(data_augmented) > 0:
        print("\n[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] BUFFER FINAL | " + str(args.target_file) + "\n")
        write_data(args.target_file, data_augmented)

    register_log('Process finished.', print_msg=True)