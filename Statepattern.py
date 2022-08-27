from state_machine import (State, Event, acts_as_state_machine,
                           after, before, InvalidStateTransition)
from abc import ABC, abstractmethod
import random

@acts_as_state_machine
class CheckoutProcess:
    # define 5 states
    checkout = State(initial=True)
    payment = State()
    pending = State()
    confirmed = State()
    canceled = State()

    # define transitions
    beginCheckout = Event(from_states= checkout, to_state = payment)
    submit = Event(from_states=payment, to_state = pending)
    approve = Event(from_states = pending, to_state = confirmed)
    cancel = Event(from_states = confirmed, to_state = canceled)
    disapprove = Event(from_states = pending, to_state = checkout)
    back = Event(from_states = (confirmed, canceled), to_state = checkout)

    def __init__(self, name):
        self.name = name

    @after('beginCheckout')
    def beginCheckout_info(self):
        print(f'{self.name} said please enter your credit card information')
    
    @after('submit')
    def submit_info(self):
        print(f'{self.name} received the order request and we are verifying your order')
        
    @after('cancel')
    def cancel_info(self):
        print(f'{self.name} said sorry to hear you cancel your order, but I am glad to help')
    
    @after('back')
    def back_info(self):
        print(f'{self.name} said good to see you coming back')
 

class OrderSystem:
    def __init__(self):
        self.process = CheckoutProcess('Alex')

    def beginCheckout(self):
        try:
            self.process.beginCheckout()
        except InvalidStateTransition as err:
            print(f'Error: {self.process.name} cannot enter payment into in {self.process.current_state} state')

    def gotOrder(self):
        try:
            self.process.submit()
            self.verifyOrder()
        except InvalidStateTransition as err:
            print(f'Error: {self.process.name} said sorry your order was not approved, please remove some items in your shopping cart.')
    
    def verifyOrder(self):
        approved = random.randint(0,9) >3
        try:
            if approved == True:
                self.process.approve()
            else:
                self.process.disapprove()
        except InvalidStateTransition as err:
        
            print(f'{self.process.name} cannot enter confirmed state in {self.process.current_state} state')
    
    def cancelOrder(self):
        try:
            self.process.cancel()
        except InvalidStateTransition as err:
            print(f'Error:  {self.process.name} cannot cancel your order in payment state')
    
    def back(self):
        try:
            self.process.back()
        except InvalidStateTransition as err:
            print(f'Error: {self.process.name} cannot return to checkout in payment state')


def showMenu():
    print("COMMAND MENU")
    print("begin - Begin Checkout")
    print("submit - Submit your order")
    print("cancel - Cancel my order")
    print("return - Back to Checkout")
    print("exit - Exit program")
    print() 
        
def main():
    mall = OrderSystem() 
    showMenu()
    
    while True:        
        command = input("Command: ")
        if command == "begin":
            mall.beginCheckout()
        elif command == "submit":
            mall.gotOrder()
        elif command == "cancel":
            mall.cancelOrder()
        elif command == "return":
            mall.back()
        elif command == "exit":
            print("Bye!")
            break
        else:
            print("Not a valid command. Please try again.\n")
            
    
if __name__ == "__main__":
    main()
    