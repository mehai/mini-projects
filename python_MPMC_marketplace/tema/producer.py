"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, daemon=kwargs['daemon'])
        self.marketplace = marketplace
        self.products = products
        self.republish_wait_time = republish_wait_time
        self.name = kwargs['name']

    def run(self):
        prod_id = self.marketplace.register_producer()
        while True:
            for product in self.products:
                quantity = product[1]
                while quantity > 0:
                    produce(product)
                    while not self.marketplace.publish(producer_id=prod_id, product=product[0]):
                        sleep(self.republish_wait_time)
                    quantity -= 1

def produce(product):
    """
    simulates production of given product by sleeping
    the production time of product.

    :param product: tuple containing production time
    """
    sleep(product[2])
