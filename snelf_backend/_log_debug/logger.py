import datetime

def erase():
    with open("_log_debug/log.txt", 'w') as f:
        f.close()

def log(line: str):
    with open("_log_debug/log.txt", 'a') as f:
        f.write("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + line + "\n")
        f.close()

def lastLine():
    with open("_log_debug/log.txt", 'r') as f:
        linhas = f.readlines()
        linhas.reverse()
        f.close()
        return linhas[0]