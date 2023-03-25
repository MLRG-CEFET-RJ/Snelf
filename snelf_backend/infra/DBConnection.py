import psycopg2

class DBConnection:
    _self = None
    connection = None
    cursor = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)

            database = "testejp"
            user = "testejp"
            password = "testejp"
            host = "snelf-postgres"
            port = "5432"

            def tryToConnect():
                try:
                    cls._self.connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
                    print("back conectado ao banco pela porta 5432")
                except Exception as e:
                    try:
                        print("conexão com o banco na porta 5432 falhou")
                        cls._self.connection = psycopg2.connect(database=database, user=user, password=password, host="localhost", port="54320")
                        print("back conectado ao banco pela porta 54320")
                    except Exception as e2:
                        print("conexão com o banco na porta 54320 falhou")
                        tryToConnect()

            tryToConnect()
            cls._self.connection.autocommit = True
            cls._self.cursor = cls._self.connection.cursor()

        return cls._self


