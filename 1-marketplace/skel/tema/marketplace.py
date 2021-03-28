"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
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

        self.no_of_producer = 0
        self.producers = {}
        self.reg_producer_lock = Lock()

        self.no_of_cart = 0
        self.costumers = {}
        self.new_cart_lock = Lock()

        self.add_cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.reg_producer_lock:
            self.no_of_producer += 1
            self.producers[self.no_of_producer] = []
            return self.no_of_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # checking the size of the producer_id's buffer
        if len(self.producers[int(producer_id)]) >= self.queue_size_per_producer:
            return False

        self.producers[int(producer_id)].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            self.no_of_cart += 1
            self.costumers[self.no_of_cart] = []
            return self.no_of_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        for i in self.producers:
            if product in self.producers[i]:
                # remove the product from the respective producer...
                with self.add_cart_lock:
                    self.producers[i].remove(product)
                # ... and add the product to the respective consumer
                self.costumers[cart_id].append([i, product])
                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        for producer in self.costumers[cart_id]:
            if product == producer[1]:
                # add the product to the respective producer...
                self.producers[producer[0]].append(product)
                # remove the product from the respective consumer
                self.costumers[cart_id].remove(producer)
                return True

        return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        items_bought = []
        # creating the list with products of cart_id
        for producer in self.costumers[cart_id]:
            items_bought.append(producer[1])

        return items_bought
