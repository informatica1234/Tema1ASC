"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


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
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs["name"]
        self.id_consumer = self.marketplace.new_cart()

    def run(self):
        for cart in self.carts:
            for action in cart:
                i = 0
                # calling "add_to_cart" function
                if action["type"] == "add":
                    while i < action["quantity"]:
                        if self.marketplace.add_to_cart(self.id_consumer, action["product"]):
                            i += 1
                        else:
                            time.sleep(self.retry_wait_time)
                # calling "remove_from_cart" function
                else:
                    while i < action["quantity"]:
                        if self.marketplace.remove_from_cart(self.id_consumer, action["product"]):
                            i += 1
                        else:
                            time.sleep(self.retry_wait_time)
        # receive all products bought
        items_bought = self.marketplace.place_order(self.id_consumer)
        for product in items_bought:
            print("{} bought {}".format(self.name, product))
