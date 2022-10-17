import time
import click
from src.model.family_wallet import *

def exitconsole():
    time.sleep(0.1)
    exit()    

@click.group
def cli():
    pass

@click.command
@click.option('--username', help= "Provide username", prompt= True)
@click.option('--password', help= "Provide password", prompt= True)
def open_wallet(username, password):
    '''This function checks the credentials provided and provides all available options to authorized users'''
    userCheck = User()
    user = userCheck.check_credentials(username.strip(), password.strip(), os.path.join(FILES_DIR_NAME, USERS_JSON))
    if user is not None:
        if user.get('status').upper() == BLOCKED:
            print("-"*50, end="\n\n")
            print('Sorry. Your account is blocked\n')
            print("-"*50, end="\n")
            exitconsole()
        profile = user.get('profile')
        if profile and profile in ALLOWED_ACTIONS.keys():
            wallet = FamilyWallet()
            print(f"\nWelcome {user.get('username').capitalize()},")
            current_balance = 0
            transaction_path = wallet.get_transaction_path()
            transaction = Transaction()
            while True:
                if os.path.exists(transaction_path):
                    current_balance = transaction.fetch_current_balance(transaction_path)
                if current_balance < 100 and profile in PARENTS:
                    print("\n\tWARNING: Your current balance is low. Please add more funds")
                time.sleep(0.4)
                print('\n>> Please choose from options below: ')
                options_list = ALLOWED_ACTIONS.get(profile)
                for i, item in enumerate(options_list):
                    print(f"\t{i+1}. {ALL_ACTIONS.get(item)}")
                try:
                    choice = int(input(f"Your option as a number between 1-{len(options_list)}: "))
                    match options_list[choice - 1]:
                        case "MAKE_PAYMENT":
                            wallet.make_payment(user)
                        case "VIEW_PENDING_REQUESTS":
                            wallet.show_pending_requests(user)
                        case "VIEW_ALL_TRANSACTIONS":
                            wallet.show_all_transactions(profile)
                        case "BLOCK":
                            wallet.block_user()
                        case "VIEW_BALANCE":
                            wallet.show_current_balance(user)
                        case "ADD_FUNDS":
                            wallet.add_funds(user, None)
                        case "WITHDRAW":
                            wallet.withdraw_funds(user)
                        case "EXIT":
                            break
                        case _:
                            print(f"Please choose a number between 1-{len(options_list)} ")
                    choice = 0
                except:
                    print(f'Invalid input. Please choose an option as a number between 1-{len(options_list)} ')  
            exitconsole()          
        else:
            print('Unable to process request. Check wallet profiles.')    
    else:
        print("-"*50, end="\n\n")
        print('Invalid credentials! Try again\n')
        print("-"*50, end="\n")
        exitconsole()
