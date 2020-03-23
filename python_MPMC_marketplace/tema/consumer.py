"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.marketplace = marketplace
        self.carts = carts
        self.retry_wait_time = retry_wait_time
        self.name = kwargs['name']

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for operation in cart:
                self.execute_operation(cart_id=cart_id, operation=operation)
            items = self.marketplace.place_order(cart_id)
            self.consume(items)

    def execute_operation(self, cart_id, operation):
        """
        Method used to execute an operation.

        :param cart_id: the id of the currently used cart
        :param operation: the operation to be executed in the marketplace
        """
        op_type = operation['type']
        quantity = operation['quantity']
        product = operation['product']
        if op_type == 'add':
            while quantity > 0:
                while not self.marketplace.add_to_cart(cart_id=cart_id, product=product):
                    sleep(self.retry_wait_time)
                quantity -= 1
        elif op_type == 'remove':
            while quantity > 0:
                self.marketplace.remove_from_cart(cart_id=cart_id, product=product)
                quantity -= 1

    def consume(self, items):
        """
        Prints the received bought items by this consumer.

        :param items: list of tuples [Product, quantity]
        """
        for item, quantity in items:
            for _ in range(quantity):
                print(f'{self.name} bought {item}')
