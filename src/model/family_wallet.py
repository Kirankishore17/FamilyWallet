from datetime import datetime
import os
from src.model.pending_request import Request
from src.model.transaction import Transaction
from src.model.user import User

SOURCE_DIR = os.path.join(os.getcwd(), "src")
FILES_DIR_NAME = os.path.join(os.getcwd(), "src", "files")

TRANSACTIONS_JSON = "transactions.json"
USERS_JSON = "users.json"
PENDING_REQUEST_JSON = "pending_request.json"

PARENTS = ["MOM", "DAD"]
BLOCKED = "BLOCKED"
ACTIVE = "ACTIVE"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
ALLOWED_ACTIONS = {"CHILD" : ["MAKE_PAYMENT", "VIEW_PENDING_REQUESTS", "VIEW_BALANCE", "EXIT"],
                    "MOM" : ["ADD_FUNDS", "WITHDRAW", "MAKE_PAYMENT", "VIEW_PENDING_REQUESTS", "VIEW_ALL_TRANSACTIONS" ,"VIEW_BALANCE", "EXIT"],
                    "DAD" : ["ADD_FUNDS", "WITHDRAW", "MAKE_PAYMENT", "VIEW_PENDING_REQUESTS", "VIEW_ALL_TRANSACTIONS" , "BLOCK", "VIEW_BALANCE", "EXIT"]}
ALL_ACTIONS = {"MAKE_PAYMENT" : "Make Payment", "VIEW_PENDING_REQUESTS" : "View Pending Requests", "VIEW_BALANCE" : "View Current Balance", "VIEW_ALL_TRANSACTIONS" : "View All Past Transactions", "BLOCK" : "Block A User", "EXIT" : "Sign Out", "ADD_FUNDS" : "Add Funds", "WITHDRAW" : "Withdraw Funds" }

class FamilyWallet:
    def get_transaction_path(self):
        return os.path.join(FILES_DIR_NAME, TRANSACTIONS_JSON)

    def get_user_profiles_path(self):
        return os.path.join(FILES_DIR_NAME, USERS_JSON)

    def get_pending_requests_path(self):
        return os.path.join(FILES_DIR_NAME, PENDING_REQUEST_JSON)

    def get_current_balance(self):
        transaction_path = self.get_transaction_path()
        transaction = Transaction()
        if os.path.exists(transaction_path):
            return transaction.fetch_current_balance(transaction_path)
        return None

    def show_current_balance(self,user):
        '''This function displays current balance'''
        transaction_path = self.get_transaction_path()
        transaction = Transaction()
        print("="*50, end="\n\n")
        amount = transaction.fetch_current_balance(transaction_path)
        if os.path.exists(transaction_path):
            print(f"\tWallet Balace: ${amount}\n")
        else:
            print(f"\tWallet Balace: 0")
            with open(transaction_path, 'w') as file:
                file.write('[]')
        print("="*50, end="\n\n")
        if amount == 0 and user.get('profile').upper() == "CHILD":
            choice = input('Current balance is 0. Do you want to request parents to add funds? (y/n) ')
            if choice.upper() == 'Y':
                self.request_add_funds(user)

    def request_add_funds(self,user):
        '''This function allows CHILD to raise a new request to add more funds'''
        try:
            request = Request()
            entry = {}
            entry['_from'] = user.get('username')
            entry['_to'] = ["MOM", "DAD"]
            entry['description'] = "to add funds"
            entry['action'] = "ADD_FUNDS"
            entry['amount'] = ""
            entry['timestamp'] = datetime.now().strftime(DATE_FORMAT)
            request.append_file(entry, self.get_pending_requests_path())
            print('Successfully raised request.')
        except:
            print('Unable to create new request.')

    def withdraw_funds(self, user):
        '''This function allows parents to withdraw funds'''
        profile = user.get('profile')
        username = user.get('username')
        if profile in PARENTS:
            choice = input('Would you like to withdraw funds? (y/n) ')
            if choice.upper() == 'Y':
                try:
                    amount = int(input('Please provide the amount: '))
                    if self.get_current_balance() - amount < 0:
                        print('Insufficient funds')
                        return
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    transaction_path = self.get_transaction_path()
                    transaction = Transaction()
                    description = f"withdrew ${amount}"
                    transaction.update_transaction(username, -1 * amount, date, description, transaction_path)
                    print(f'Successfully withdrew ${amount}.')
                except:
                    print('Invalid input. Amount must be a whole number more than 0')            
            else:
                choice = input('Do you want to exit payment? (y/n) ')
                if choice.upper() == 'Y':
                    return

    def show_all_transactions(self, profile):
        '''This function is used to display all past transactions'''
        transaction_path = self.get_transaction_path()
        transaction = Transaction()
        if os.path.exists(transaction_path) and profile in PARENTS:
            view_list = [f"{x.get('user')} {x.get('description')} on {x.get('timestamp')}" for x in transaction.read_file(transaction_path)]
            print("-"*50, end="\n\n")
            print('Past Transactions are:', end="\n\t")
            print(*view_list, sep = "\n\t", end="\n\n")
            print("-"*50, end="\n\n")
        else:
            print('\t***No transactions found***')

    def request_overspend(self, user, amount):
        '''This function allows CHILD to raise a new request to spend more than $50'''
        try:
            request = Request()
            entry = {}
            entry['_from'] = user.get('username')
            entry['_to'] = ["MOM"]
            entry['description'] = f"to over spend ${amount}"
            entry['amount'] = amount
            entry['action'] = "OVERSPEND"
            entry['timestamp'] = datetime.now().strftime(DATE_FORMAT)
            request.append_file(entry, self.get_pending_requests_path())
            print('Successfully raised request.')
        except:
            print('Unable to create new request.')
        
    def request_multispend(self, user):
        '''This function allows CHILD to raise a new request to spend more than once a day'''
        try:
            request = Request()
            entry = {}
            entry['_from'] = user.get('username')
            entry['_to'] = ["MOM", "DAD"]
            entry['description'] = "to multi spend"
            entry['action'] = "MULTISPEND"
            entry['amount'] = ""
            entry['timestamp'] = datetime.now().strftime(DATE_FORMAT)
            request.append_file(entry, self.get_pending_requests_path())
            print('Successfully raised request.')
        except:
            print('Unable to create new request.')

    def block_user(self):
        '''This function is used to block a user'''
        userObj= User()
        path = self.get_user_profiles_path()
        users_list = userObj.read_file(path)
        try:
            active_users = list(filter(lambda x: (x.get('status') == ACTIVE), users_list))
            print('Active users:')
            for i in range(len(active_users)):
                print(f"{i+1}. {active_users[i].get('username')}")
            choice = int(input('Choose account to block as a number: '))
            if choice < len(users_list) and choice > 0:
                confirm = input(f"Are you sure you want to block {active_users[choice-1].get('username')}? (y/n) ")
                if confirm.upper() == 'Y':
                    for i, item in enumerate(users_list):
                        if item.get('username') == active_users[choice-1].get('username'):
                            pos = i
                    updated_user = users_list[pos]
                    del users_list[pos]
                    updated_user['status'] = BLOCKED
                    users_list.append(updated_user)
                    userObj.update_profiles(users_list, path)
                    print('>>  Account successfully blocked  <<')
                    return
            else:
                print('Invalid choice.')
                return
        except:
            print('Unable to block account')    

    def make_payment(self, user):
        '''This function allows users to make payment'''
        profile = user.get('profile')
        username = user.get('username')
        try:
            amount = int(input('Please provide the amount: '))
            if self.get_current_balance() - amount < 0:
                print('Insufficient funds')
                return
            if profile.upper() == "CHILD":
                diff_period = datetime.now() - datetime.strptime(user.get('last_spent'), DATE_FORMAT)
                if (diff_period.days <= 1) and (user.get('allow_multi_spend').upper() == "FALSE"):
                    print('You do not have permission to spend more than once a day. ')
                    child_choice = input(f'Would you like to raise a request to multispend? (y/n) ')
                    if child_choice.upper() == 'Y':
                        return self.request_multispend(user)
                    else:
                        return
                elif (amount > int(user.get('credit_limit')) and user.get('allow_overspend').upper() == "FALSE"):
                    print('You do not have permission to spend more than $50. ')
                    child_choice = input(f'Would you like to raise a request to overspend ${amount}? (y/n) ')
                    if child_choice.upper() == 'Y':
                        return self.request_overspend(user, amount)
                    else:
                        return
                else:
                    if self.get_current_balance() - amount < 0:
                        print('\n\nInsufficient funds')
                        return
            merchant = input('Provide retail merchant name: ')
            date = datetime.now().strftime(DATE_FORMAT)
            transaction_path = self.get_transaction_path()
            transaction = Transaction()
            description = f"spent ${amount} at {merchant}"
            transaction.update_transaction(username, -1 * amount, date, description, transaction_path)
            if profile.upper() == "CHILD":
                userObj= User()
                users_list = userObj.read_file(self.get_user_profiles_path())
                user['last_spent'] = date
                for i in range(len(users_list)):
                    if users_list[i]['username'] == user['username']:
                        pos = i
                if (amount > 50) and (user.get('allow_overspend').upper() == "TRUE"):
                    user['allow_overspend'] = "false"
                    user['credit_limit'] = "50"
                if (diff_period.days <= 1) and (user.get('allow_multi_spend').upper() == "TRUE"):
                    user['last_spent'] = date
                    user['allow_multi_spend'] = "false"
                del users_list[pos]
                users_list.append(user)
                userObj.update_profiles(users_list, self.get_user_profiles_path())
            print("="*50, end="\n\n")
            print('\tPayment Successful\n')
            print("="*50, end="\n\n")
        except:
            print('Unable to make payment.')            

    def add_funds(self,user, request):
        '''This function allows a parent to add funds into the wallet'''
        profile = user.get('profile')
        username = user.get('username')
        if profile in PARENTS:
            # current_balance = 0
            transaction_path = self.get_transaction_path()
            transaction = Transaction()
            choice = input('Would you like to add funds to the wallet? (y/n) ')
            if choice.upper() == 'Y':
                amount = None
                while True:
                    try:
                        amount = int(input('Enter amount to be deposited into the wallet? '))
                        if amount <=0:
                            raise Exception("Sorry, no numbers below zero") 
                        description = f"added ${amount} to wallet"
                        transaction.update_transaction(username, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description, transaction_path)
                        print(f"\n\n>> >> Successfully added ${amount} to the wallet. << <<\n")
                        return None
                    except ValueError:
                        print('\tInvalid input. Amount must be a whole number greater than 0')
            else:
                choice = input('Do you want to exit? (y/n) ')
                if choice.upper() == 'Y':
                    return request
                else:
                    return None        

    def handle_request(self, user, request):
        '''This function handles request raised by CHILD'''
        if request.get('action') == "ADD_FUNDS":
            return self.add_funds(user, request)
        elif request.get('action') == "OVERSPEND":
            print(f"--->  A request was raised to overspend funds by {request.get('_from')} on {request.get('timestamp')}")
            choice = input('Do you want to delete this request? (y/n) ')
            if choice.upper() == 'Y':
                return None
            choice = input('Would you like to reassign this task to DAD? (y/n) ')
            if choice.upper() == 'Y':
                return self.reassign(user, request)
            userObj = User()
            users_list = userObj.read_file(self.get_user_profiles_path())
            for i in range(len(users_list)):
                if users_list[i]['username'] == user['username']:
                    pos = i
            choice = input(f"Do you want to allow {request.get('_from')} to overspend {request.get('amount')}? (y/n) ")
            if choice.upper() == 'Y':
                del users_list[pos]
                user['allow_overspend'] = "true"
                user['credit_limit'] = request.get('amount')
                users_list.append(user)
                userObj.update_profiles(users_list, self.get_user_profiles_path())
                return None
        elif request.get('action') == "MULTISPEND":
            print(f"--->  A request was raised to spend more than once a day by {request.get('_from')} on {request.get('timestamp')}")
            choice = input('Do you want to delete this request? (y/n) ')
            if choice.upper() == 'Y':
                return None
            userObj = User()
            users_list = userObj.read_file(self.get_user_profiles_path())
            for i in range(len(users_list)):
                if users_list[i]['username'] == user['username']:
                    pos = i
            choice = input(f"Do you want to allow {request.get('_from')} to multispend {request.get('amount')}? (y/n) ")
            if choice.upper() == 'Y':
                del users_list[pos]
                user['allow_multi_spend'] = "true"
                users_list.append(user)
                userObj.update_profiles(users_list, self.get_user_profiles_path())
                return None
        return request

    def reassign(self, user, request):
        '''This function allows MOM to reassign a request to DAD'''
        profile = user.get('profile')
        username = user.get('username')
        if profile in PARENTS:
            choice = input('Would you like to reassign this task to DAD? (y/n) ')
            if choice.upper() == 'Y':
                try:
                    request['_to'] = ["DAD"]
                    print('Request reassigned to DAD')
                    return request
                except:
                    print('\tUnable to reassign pending task')
            else:
                choice = input('Do you want to exit? (y/n) ')
                if choice.upper() == 'Y':
                    return request
                else:
                    return request        

    def show_pending_requests(self,user):
        '''This functions displays pending requests'''
        profile = user.get('profile')
        username = user.get('username')
        pending_request_path = self.get_pending_requests_path()
        if os.path.exists(pending_request_path):
            pending_request = Request()
            list = pending_request.fetch_pending_requests(pending_request_path)
            updated_list = []
            view_list = [f"To {x.get('description')} on {x.get('timestamp')}" for x in list if x.get('_from').lower() == username.lower()]
            if profile not in PARENTS and len(view_list) > 0:
                print("-"*50, end="\n\n")
                print('Your pending requests are:', end="\n\t")
                print(*view_list, sep = "\n\t", end="\n\n")
                print("-"*50, end="\n\n")
            else:
                print(f"==>\tYou have {len(list)} pending request.", end="\n\n")
                for request in list[::-1]:
                    if profile in request.get("_to"):
                        request = self.handle_request(user, request)
                    if request:
                        updated_list.append(request)
                pending_request.save_pending_transactions(updated_list[::-1], pending_request_path)
        else:
            with open(pending_request_path, 'w') as file:
                file.write('[]')
            self.show_pending_requests(profile)

