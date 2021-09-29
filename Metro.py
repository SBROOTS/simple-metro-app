import datetime
from uuid import uuid4
from Exceptions import *


class Ticket:
    def __init__(self, card_type):
        self.type = card_type
        self.cid = str(uuid4())[24:36]

    def __repr__(self):
        return f'{self.cid}-{self.type}'


class Person:
    def __init__(self, first_name, last_name, card):
        self.uid = str(uuid4())[28:36]
        self.first_name = first_name
        self.last_name = last_name
        self.cards = [card]

    @property
    def show_cards(self):
        """
        :return:
        """
        cards = []
        for card in self.cards:
            if isinstance(card, MOtcCredit):
                cards.append({
                    'card ID': card.cid,
                    'card Type': card.type,
                    'card Status': 'VALID' if card.status else 'NOT VALID'
                })
            elif isinstance(card, MTimeCredit):
                cards.append({
                    'card ID': card.cid,
                    'card Type': card.type,
                    'card Balance': card.balance,
                    'Expire Time': str(card.expire_time)[:19]
                })
            else:
                cards.append({
                    'card ID': card.cid,
                    'card Type': card.type,
                    'card Balance': card.balance
                })
        return cards

    def buy_ticket(self, in_ticket):
        """
         To buy tickets
        :return: operation status
        """
        len_cards = len(self.cards)
        self.cards.append(in_ticket)
        if len(self.cards) > len_cards:
            return f"A {in_ticket.type} ticket was purchased successfully"
        else:
            return f"A {in_ticket.type} ticket wasn't purchased successfully"


class Station:
    ticket_cost = 2500

    @staticmethod
    def checkout(person, card_number):
        """
        for using ticket
        :param person: is a object from Person class
        :param card_number: index of card
        :return: result of operation
        """
        if isinstance(person, Person):
            if isinstance(person.cards[card_number], MOtcCredit):
                if person.cards[card_number].status:
                    person.cards[card_number].status = False
                    print(f"{person.first_name}  traveled with One Way Ticket ")
                    return person.cards[card_number].status
                else:
                    raise NotValidCredit("Card Not Valid")

            else:
                now = datetime.datetime.now()
                if isinstance(person.cards[card_number], MTimeCredit):
                    if person.cards[card_number].expire_time > now:
                        if person.cards[card_number].balance >= 2500:
                            person.cards[card_number].balance -= Station.ticket_cost
                            print(f"{person.first_name}  traveled with TimeCredit Ticket ")
                            return person.cards[card_number].balance
                        else:
                            raise BalanceNotEnough("your Balance Not Enough for Checkout!!")
                    else:
                        raise TimeExpiredCredit("Card Time has Expired")
                else:
                    if person.cards[card_number].balance >= 2500:
                        person.cards[card_number].balance -= Station.ticket_cost
                        print(f"{person.first_name}  traveled with Credit Ticket ")
                        return person.cards[card_number].balance
                    else:
                        raise BalanceNotEnough("your Balance Not Enough for Checkout!!")

    @staticmethod
    def increase_balance(person, card_number, amount, time_amount = 0):
        """
        for increasing balance or Expiration time
        :param card_number: index of card
        :param person: is a object from Person class
        :param amount: incoming amount from user to add to balance
        :param time_amount: if user want increase his time he can enter a value to increase expire time
        :return: result of operation
        """
        if isinstance(person, Person):
            if isinstance(person.cards[card_number], MTimeCredit):
                person.cards[card_number].balance += int(amount)
                person.cards[card_number].expire_time += datetime.timedelta(days = int(time_amount))
                print(
                    f"your Ticket balance increase to {person.cards[card_number].balance} and your Expire time extended to {person.cards[card_number].expire_time}")
                return person.cards[card_number].balance, person.cards[card_number].expire_time.day
            elif isinstance(person.cards[card_number], MCredit):
                person.cards[card_number].balance += int(amount)
                print(f"your Ticket balance increase to {person.cards[card_number].balance}")
                return person.cards[card_number].balance
            else:
                raise NotChargeable


class MCredit(Ticket):
    def __init__(self, card_type, balance):
        super().__init__(card_type)
        self.balance = balance


class MTimeCredit(Ticket):
    def __init__(self, card_type, balance, time):
        super().__init__(card_type)
        self.balance = balance
        self.expire_time = time

    @classmethod
    def create(cls, card_type, balance, time = 7):
        """
        Get time now and set the card expiration date based on the input time
        :param card_type: type of card
        :param time: a int carrying a amount of day into expiration since today (default=7 days)
        :param balance: input balance from user
        :return: result of creation
        """
        now = datetime.datetime.now()
        expire_time = now + datetime.timedelta(days = int(time))
        return cls(card_type, balance, expire_time)


class MOtcCredit(Ticket):
    def __init__(self, card_type):
        super().__init__(card_type)
        self.status = True

# if __name__ == '__main__':
# if os.path.exists("db.pkl"):
#     with open("db.pkl", "rb") as reader:
#         data = pickle.load(reader)
# else:
#     data = []
#
#
# def get_person():
#     first_name = input("Enter your first name: ")
#     last_name = input("Enter your last name: ")
#     return first_name, last_name
#
#
# def select_ticket():
#
#     print("""
#           1. One Way Ticket
#           2. Time-Credit Ticket
#           3. Credit ticket
#           """)
#     selected_ticket = int(input("Enter Your choose(1-3): "))
#     if selected_ticket == 1:
#         return MOtcCredit(card_type = "OT")
#     elif selected_ticket == 2:
#         balance = int(input("Enter your balance:"))
#         time = int(input("Select card validity period(1-30): "))
#         return MTimeCredit.create(card_type = "TC", balance = balance, time = time)
#     elif selected_ticket == 3:
#         balance = int(input("Enter your balance:"))
#         return MCredit(card_type = "C", balance = balance)
#
#
# def pick_person():
#     for index, person in enumerate(data):
#         print(f"{index}. {person.first_name} {person.last_name}")
#     person_index = int(input(f"Select a user by number 1-{len(data)}: "))
#     return data[person_index - 1]
#
#
# def pick_ticket(picked_person):
#     local_tickets = picked_person.show_cards
#     for index, ticket in enumerate(local_tickets):
#         print("-------------------------")
#         print(f"{index}.{ticket}")
#     ticket_index = int(input(f"Select a user by number 0-{len(local_tickets)}: "))
#     return ticket_index - 1
# while True:
#     if len(data) == 0:
#         print("you should create a user")
#         person_info = get_person()
#         ticket = select_ticket()
#         data.append(Person(first_name = person_info[0], last_name = person_info[1], card = ticket))
#         os.system('cls')
#     else:
#         picked_person = pick_person()
#         os.system('cls')
#         print("""
#     1.Buy a Ticket
#     2.Show Owned Tickets
#     3.Travel
#     4.Exit
#     """)
#         selected = int(input("enter your task:"))
#         if selected == 1:
#             ticket = select_ticket()
#             picked_person.buy_ticket(ticket)
#         elif selected == 2:
#             tickets = picked_person.show_cards
#             for ticket in tickets:
#                 print(ticket)
#         elif selected == 3:
#             ticket_index = pick_ticket(picked_person)
#             try:
#
#                 Station.checkout(picked_person, ticket_index)
#             except NotValidCredit:
#                 print("your ticket is not Valid!!!")
#             except TimeExpiredCredit:
#                 print("Time of your ticket has Expired")
#             except BalanceNotEnough:
#                 print("your Ticket Balance Not Enough for Travel . \n please Charge your Ticket")
#         elif selected == 4:
#             with open("db.pkl", "wb") as writer:
#                 pickle.dump(data, writer)
#             exit()
