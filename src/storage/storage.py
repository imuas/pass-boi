import os

DATA_DIR = "../data/"
USERS_FILE = DATA_DIR + "users.list"

def readFile(filename: str) -> str:
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data

def readFileb(filename: str) -> bytes:
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data

def createFile(filename: str):
    open(filename, 'w')
    return

def writeToFile(filename: str, data: str):
    with open(filename, 'w') as f:
        f.write(data)
    return

def writeToFileb(filename: str, data: bytes):
    with open(filename, 'wb') as f:
        f.write(data)
    return

def deleteFile(filename: str):
    os.remove(filename)
    return

def getUserFile(user: str) -> str:
    return DATA_DIR + user + ".pwd"