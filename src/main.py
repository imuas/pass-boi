from storage import storage, crypto
from cryptography.fernet import Fernet

USERS = dict()
CURRENT_USER = None
UPDATED_USERS = set()
KEY = None
FERNET_OBJ = None

def expectInput() -> str:
    return input("[" + CURRENT_USER + "] >> " if CURRENT_USER != None else "[NotLoggedIn] >> ")

def usage():
    print("""
[ USAGE ]
--------------------------------------------------------------------------------------------
login user      =   login Username
logout user     =   logout
create user     =   new user Username
delete user     =   delete user Username
add password    =   new password "github" "password"
get password    =   get password "github"
update password =   update password "github" "old-password" "new-password"
delete password =   delete password "github" "password"
get keys        =   get keys
get users       =   get users
--------------------------------------------------------------------------------------------
    """)

def parseFlags(flags: [str]):
    global CURRENT_USER

    if flags[0] == "login":
        if flags[1] in USERS:
            CURRENT_USER = flags[1]
            # loading passwords of this user
            enc_passwords = storage.readFileb(storage.getUserFile(CURRENT_USER))
            if len(enc_passwords) != 0:
                passwords = FERNET_OBJ.decrypt(enc_passwords).decode('utf-8')
                passwords = passwords.splitlines()
                for password in passwords:
                    key, value = password.split(" = ", 1)
                    USERS[CURRENT_USER][key] = value
        else:
            print("User Does Not Exist...")
    elif flags[0] == "logout":
        if CURRENT_USER != None:
            CURRENT_USER = None
        else:
            print("Already Logged Out...")
    elif flags[0] == "new":
        if flags[1] == "user":
            if flags[2] not in USERS:
                storage.createFile(storage.getUserFile(flags[2]))
                USERS[flags[2]] = dict()
                UPDATED_USERS.add(CURRENT_USER)
            else:
                print("User Already Exists... ")
        elif flags[1] == "password":
            if flags[2] not in USERS[CURRENT_USER]:
                USERS[CURRENT_USER][flags[2]] = flags[3]
                UPDATED_USERS.add(CURRENT_USER)
            else:
                print("Password for this key already exists...")
        else:
            usage()
    elif flags[0] == "get":
        if flags[1] == "users":
            for i, user in enumerate(USERS.keys()):
                print("[" + str(i + 1) + "]:", user)
        elif flags[1] == "password":
            if CURRENT_USER != None:
                if flags[2] in USERS[CURRENT_USER]:
                    print(flags[2] + " : " + USERS[CURRENT_USER][flags[2]])
                else:
                    print("No such key present...")
            else:
                print("Login to use this functionality...")
        elif flags[1] == "keys":
            if CURRENT_USER != None:
                for passwords in USERS[CURRENT_USER]:
                    print(passwords)
            else:
                print("Login to use this functionality...")
        else:
            usage()
    elif flags[0] == "update" and flags[1] == "password":
        if CURRENT_USER != None:
            if flags[2] in USERS[CURRENT_USER]:
                if flags[3] == USERS[CURRENT_USER][flags[2]]:
                    USERS[CURRENT_USER][flags[2]] = flags[4]
                    UPDATED_USERS.add(CURRENT_USER)
                else:
                    print("Did not update as password did not match...")
            else:
                print("Key does not exist...")
        else:
            print("Login to use this functionality...")
    elif flags[0] == "delete":
        if flags[1] == "user":
            if flags[2] in USERS:
                storage.deleteFile(storage.DATA_DIR + flags[2] + ".pwd")
                USERS.pop(flags[2])
                if CURRENT_USER == flags[2]:
                    CURRENT_USER = None
            else:
                print("User Does Not Exist...")
        elif flags[1] == "password":
            if CURRENT_USER != None:
                if flags[2] in USERS[CURRENT_USER]:
                    if flags[3] == USERS[CURRENT_USER][flags[2]]:
                        USERS[CURRENT_USER].pop(flags[2])
                        UPDATED_USERS.add(CURRENT_USER)
                    else:
                        print("Did not delete as password did not match...")
            else:
                print("Login to use this functionality...")
        else:
            usage()
    else:
        usage()

def startREPL():
    print("pass-boi REPL started !")
    print("type 'exit' to exit...")
    print("==--------------------==")
    
    while True:
        flags = expectInput().split(" ")

        if flags[0] == "exit":
            break

        parseFlags(flags)
    
    users = "\n".join(list(USERS.keys()))
    storage.writeToFile(storage.USERS_FILE, users)

    for user in USERS:
        if user in UPDATED_USERS:
            filename = storage.getUserFile(user)
            data = []
            for passwords in USERS[user]:
                temp = passwords + " = " + USERS[user][passwords]
                data.append(temp)
            data = "\n".join(data).encode()
            enc_data = FERNET_OBJ.encrypt(data)
            storage.writeToFileb(filename, enc_data)

def loadUsers():
    global KEY, FERNET_OBJ
    try:
        KEY = crypto.load_key()
    except:
        print('Creating a key.key file...')
        KEY = crypto.write_key()

    FERNET_OBJ = Fernet(KEY)

    try:
        lines = storage.readFile(storage.USERS_FILE)
        users = lines.splitlines()
        for user in users:
            USERS[user] = dict()
    except:
        storage.createFile(storage.USERS_FILE)
    return

def main():
    loadUsers()
    startREPL()


if __name__ == "__main__":
    main()
