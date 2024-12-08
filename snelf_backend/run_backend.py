import os

def run ():
  os.system("uvicorn main:app --reload --port 8000")

if __name__ == "__main__":
  run()