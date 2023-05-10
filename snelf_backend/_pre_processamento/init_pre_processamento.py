from _pre_processamento.controleDeTreinamento import ControleDeTreinamento


def run(forceRestart = False):
    from . import pre_proc_anvisa
    from _data_augmentation import init_data_augmentation
    from _move_file import move_file
    from . import pre_proc_anvisa_augmented
    from . import pre_proc_medicamentos_augmented
    from . import mapeamento_ean_chave
    from _oversampling import oversampling
    from _training import train_test_split
    import _log_debug.logger as logger

    # PRE PROCESSAMENTO 1
    if ControleDeTreinamento.running:
        if (logger.lastLine() == None or "" == logger.lastLine()) or ("pre_proc_anvisa iniciado" in logger.lastLine() or forceRestart):
            logger.erase()

            logger.log("pre_proc_anvisa iniciado")
            pre_proc_anvisa.run()
            if ControleDeTreinamento.running:
                logger.log("pre_proc_anvisa finalizado")
    

    # DATA AUGMENTATION
    if ControleDeTreinamento.running:
        if ("pre_proc_anvisa finalizado" in logger.lastLine()) or ("init_data_augmentation" in logger.lastLine()):
            logger.log("init_data_augmentation iniciado")
            init_data_augmentation.run()
            if ControleDeTreinamento.running:
                logger.log("init_data_augmentation finalizado")

    # MOVE FILES
    if ControleDeTreinamento.running:
        if ("pre_proc_anvisa finalizado" in logger.lastLine()):
            move_file.move("datasets/medicamentos/medicamentos_aumentado.csv", "datasets/medicamentos/augmented/medicamentos_aumentado.csv")
            logger.log("move_file 1")
            move_file.move("datasets/anvisa/anvisa_principio_ativo_aumentado.csv", "datasets/anvisa/augmented/anvisa_principio_ativo_aumentado.csv")
            logger.log("move_file 2")
            move_file.move("datasets/anvisa/anvisa_produto_aumentado.csv", "datasets/anvisa/augmented/anvisa_produto_aumentado.csv")
            logger.log("move_file 3")

    # PRE PROCESSAMENTO 2
    if ControleDeTreinamento.running:
        if ("move_file 3" in logger.lastLine()) or ("pre_proc_anvisa_augmented iniciado" in logger.lastLine()):
            logger.log("pre_proc_anvisa_augmented iniciado")
            pre_proc_anvisa_augmented.run()
            if ControleDeTreinamento.running:
                logger.log("pre_proc_anvisa_augmented finalizado")

    if ControleDeTreinamento.running:
        if ("pre_proc_anvisa_augmented finalizado" in logger.lastLine()) or ("pre_proc_medicamentos_augmented iniciado" in logger.lastLine()):
            logger.log("pre_proc_medicamentos_augmented iniciado")
            pre_proc_medicamentos_augmented.run()
            if ControleDeTreinamento.running:
                logger.log("pre_proc_medicamentos_augmented finalizado")

    if ControleDeTreinamento.running:
        if ("pre_proc_medicamentos_augmented finalizado" in logger.lastLine()) or ("mapeamento_ean_chave iniciado" in logger.lastLine()):
            logger.log("mapeamento_ean_chave iniciado")
            mapeamento_ean_chave.run()
            if ControleDeTreinamento.running:
                logger.log("mapeamento_ean_chave finalziado")

    # OVERSAMPLING
    if ControleDeTreinamento.running:
        if ("mapeamento_ean_chave finalziado" in logger.lastLine()) or ("oversampling iniciado" in logger.lastLine()):
            logger.log("oversampling iniciado")
            oversampling.run()
            if ControleDeTreinamento.running:
                logger.log("oversampling finalizado")

    # TRAINING
    if ControleDeTreinamento.running:
        if ("oversampling finalizado" in logger.lastLine()) or ("train_test_split iniciado" in logger.lastLine()):
            logger.log("train_test_split iniciado")
            train_test_split.run()
            if ControleDeTreinamento.running:
                logger.log("train_test_split finalizado")