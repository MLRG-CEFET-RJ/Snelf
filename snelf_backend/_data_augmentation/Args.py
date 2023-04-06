class Args:
    def __init__(self, src_file, target_file, dataset_name, request_delay = 2, use_col = 'None'):
        if dataset_name not in ('medicamentos', 'anvisa'):
            raise Exception("dataset_name precisa ser \"medicamentos\" ou \"anvisa\"")

        if dataset_name == 'anvisa' and use_col not in ('produto', 'principio_ativo'):
            raise Exception("para o dataset_name \"anvisa\", use_col precisa ser \"produto\" ou \"principio_ativo\"")

        self.src_file = src_file
        self.target_file = target_file
        self.dataset_name = dataset_name
        self.request_delay = request_delay
        self.use_col = use_col