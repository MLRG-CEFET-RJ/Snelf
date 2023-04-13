def run():
    from . import pre_proc_anvisa
    from _data_augmentation import init_data_augmentation
    from _move_file import move_file
    from . import pre_proc_anvisa_augmented
    from . import pre_proc_medicamentos_augmented
    from . import mapeamento_ean_chave
    from _oversampling import oversampling
    from _training import train_test_split
    import _log_debug.logger as logger

    logger.erase()

    # PRE PROCESSAMENTO 1
    logger.log("pre_proc_anvisa iniciado")
    pre_proc_anvisa.run()
    logger.log("pre_proc_anvisa finalizado")
    # pre_proc_medicamentos.run()

    # DATA AUGMENTATION
    logger.log("init_data_augmentation iniciado")
    init_data_augmentation.run()
    logger.log("init_data_augmentation finalizado")

    # MOVE FILES
    move_file.move("datasets/medicamentos/medicamentos_aumentado.csv", "datasets/medicamentos/augmented/medicamentos_aumentado.csv")
    logger.log("move_file 1")
    move_file.move("datasets/anvisa/anvisa_principio_ativo_aumentado.csv", "datasets/anvisa/augmented/anvisa_principio_ativo_aumentado.csv")
    logger.log("move_file 2")
    move_file.move("datasets/anvisa/anvisa_produto_aumentado.csv", "datasets/anvisa/augmented/anvisa_produto_aumentado.csv")
    logger.log("move_file 3")

    # PRE PROCESSAMENTO 2
    logger.log("pre_proc_anvisa_augmented iniciado")
    pre_proc_anvisa_augmented.run()
    logger.log("pre_proc_anvisa_augmented finalizado")
    logger.log("pre_proc_medicamentos_augmented iniciado")
    pre_proc_medicamentos_augmented.run()
    logger.log("pre_proc_medicamentos_augmented finalizado")
    logger.log("mapeamento_ean_chave iniciado")
    mapeamento_ean_chave.run()
    logger.log("mapeamento_ean_chave finalziado")

    # OVERSAMPLING
    logger.log("oversampling iniciado")
    oversampling.run()
    logger.log("oversampling finalizado")

    # TRAINING
    logger.log("train_test_split iniciado")
    train_test_split.run()
    logger.log("train_test_split finalizado")