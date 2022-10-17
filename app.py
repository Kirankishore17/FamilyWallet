import os

from src.util import (FILES_DIR_NAME, USERS_JSON, exitconsole, open_wallet)

def main():
    '''This function executes all the functionalities of the module'''
    users_file = os.path.join(FILES_DIR_NAME, USERS_JSON)
    if os.path.exists(users_file):
        open_wallet()
    else:
        print("-"*50, end="\n\n")
        print('Wallet does not have any registered users!\nCreate user profiles to use the wallet.\n\n')
        print("-"*50, end="\n\n")
        for _ in os.listdir(FILES_DIR_NAME):
            print(_)
            os.remove(os.path.join(FILES_DIR_NAME, _))
        exitconsole()

if __name__ == "__main__":
    main()
