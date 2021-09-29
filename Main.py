from Metro import *
import pickle
import os

if os.path.exists("db.pkl"):
    with open("db.pkl", "rb") as reader:
        data = pickle.load(reader)
else:
    data = []


def get_person():
    """get first name and last name from user """
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    return first_name, last_name


def select_ticket():
    """
    selecting ticket by user
    :return: a ticket object
    """
    print("""#############################
    
           1. One Way Ticket
           2. Time-Credit Ticket
           3. Credit ticket
           
           """)
    selected_ticket = int(input("Enter Your choose(1-3): "))
    if selected_ticket == 1:
        return MOtcCredit(card_type = "OT")
    elif selected_ticket == 2:
        balance = int(input("Enter your balance:"))
        time = int(input("Select card validity period(1-30): "))
        return MTimeCredit.create(card_type = "TC", balance = balance, time = time)
    elif selected_ticket == 3:
        balance = int(input("Enter your balance:"))
        return MCredit(card_type = "C", balance = balance)


def pick_person():
    """pick a user for login
    """
    for index, person in enumerate(data):
        print(f"{index}. {person.first_name} {person.last_name} -> UID:{person.uid}")
    person_index = int(input(f"Pick a user by number (0-{len(data) - 1}): "))
    return data[person_index]


def pick_ticket(picked_person):
    """pick a ticket by user"""
    local_tickets = picked_person.show_cards
    for index, ticket in enumerate(local_tickets):
        print("---------------------------")
        print(f"{index}.{ticket}")
    print("*****************************")
    ticket_index = int(input(f"Select a user by number (0-{len(local_tickets) - 1}): "))
    return ticket_index


def charge_balance():
    """get a cost for charge from user"""
    balance = int(input(f"Enter Balance you want to charge: "))
    return balance


def extend_time():
    """ get a day for Extend time from user"""
    time = int(input(f"Enter time you want to Extend time(1-30): "))
    return time


if __name__ == '__main__':
    if len(data) == 0:
        print("you should create a user")
        person_info = get_person()
        ticket = select_ticket()
        data.append(Person(first_name = person_info[0], last_name = person_info[1], card = ticket))
        with open("db.pkl", "wb") as writer:
            pickle.dump(data, writer)
        os.system('cls')
        # read_one_time = True
    else:

        picked_person = pick_person()
        # read_one_time = True
        # os.system('cls||clear')
    while True:
        print(
            f"""#############################

             \033[92m # Welcome {picked_person.first_name} {picked_person.last_name} -> UID:{picked_person.uid} ##\n\033[0m
            1.Buy a Ticket
            2.Show Owned Tickets
            3.Travel
            4.increase Balance
            5.Add a New Person
            6.Exit
            """)
        selected = int(input("enter your task:"))
        if selected == 1:
            ticket = select_ticket()
            print(picked_person.buy_ticket(ticket))
        elif selected == 2:
            tickets = picked_person.show_cards
            for ticket in tickets:
                print(ticket)
        elif selected == 3:
            ticket_index = pick_ticket(picked_person)
            try:

                Station.checkout(picked_person, ticket_index)
            except NotValidCredit:
                print("\033[91m" + "Error:your ticket is not Valid!!!" + "\033[0m")
            except TimeExpiredCredit:
                print("\033[91m" + "Error:Time of your ticket has Expired" + "\033[0m")
            except BalanceNotEnough:
                print(
                    "\033[91m" + "Error:your Ticket Balance Not Enough for Travel . \n please Charge your Ticket" + "\033[0m")
        elif selected == 4:
            ticket = pick_ticket(picked_person)
            try:
                if not isinstance(picked_person.cards[ticket], MOtcCredit):
                    if isinstance(picked_person.cards[ticket], MTimeCredit):
                        Station.increase_balance(person = picked_person, card_number = ticket,
                                                 amount = charge_balance(),
                                                 time_amount = extend_time())
                    else:
                        Station.increase_balance(picked_person, ticket, charge_balance())
                else:
                    raise NotChargeable("One Way Ticket Not Chargeable!!")
            except NotChargeable:
                print("\033[91m" + "Error:One Way Ticket Not Chargeable!!" + "\033[0m")
        elif selected == 5:
            person_info = get_person()
            ticket = select_ticket()
            data.append(Person(first_name = person_info[0], last_name = person_info[1], card = ticket))
            print("A person Added to Database")
        elif selected == 6:
            with open("db.pkl", "wb") as writer:
                pickle.dump(data, writer)
            exit()
