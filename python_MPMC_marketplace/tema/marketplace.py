"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        #producers logic
        self.register_lock = Lock()
        self.producers = []
        #buffer
        self.producer_lock = Lock()
        self.available_products = {}
        #carts logic
        self.carts = []
        self.free_carts = []
        self.carts_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.register_lock:
            self.producers.append(0)
            return len(self.producers) - 1


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.producers[producer_id] == self.queue_size_per_producer:
            return False
        with self.producer_lock:
            if product in self.available_products:
                self.available_products[product].append(producer_id)
            else:
                self.available_products[product] = [producer_id]
            self.producers[producer_id] += 1
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.carts_lock:
            if self.free_carts:
                return self.free_carts.pop()
        new_cart = {}
        self.carts.append(new_cart)
        return len(self.carts) - 1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        if product not in self.available_products or \
            not self.available_products[product]:
            return False
        producer_id = -1
        with self.producer_lock:
            producer_id = self.available_products[product].pop()
            self.producers[producer_id] -= 1
        if product in self.carts[cart_id]:
            self.carts[cart_id][product].append(producer_id)
        else:
            self.carts[cart_id][product] = [producer_id]
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if product not in self.carts[cart_id]:
            return
        producer_id = self.carts[cart_id][product].pop()
        with self.producer_lock:
            self.producers[producer_id] -= 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = [(product, len(self.carts[cart_id][product]))
                    for product in self.carts[cart_id].keys()]
        # with self.producer_lock:
        #     for product, _ in products:
        #         for producer_id in self.carts[cart_id][product]:
        #                 self.producers[producer_id] -= 1
        self.carts[cart_id].clear()
        with self.carts_lock:
            self.free_carts.append(cart_id)
        return products
