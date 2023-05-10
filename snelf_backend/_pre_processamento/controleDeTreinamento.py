class ControleDeTreinamento:
    _self = None

    running = False

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self