import os
import warnings
import importlib
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rango.models import Seller, Users, Bids, Items, Stores, Tags

#from django.core.exceptions import ObjectDoesNotExist

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==============={os.linesep}TEST FAILURE = ({os.linesep}==============={os.linesep})"
FAILURE_FOOTER = f"{os.linesep}"

# class SellerMethodTests(TestCase):
#     def test_slug_line_creation(self):
#         seller = Sellers(userID = x, sellerName = "Bob's Premier Collection", rating = 2)
#         seller.save()

#         self.assertEqual(seller.slug, "bob's-premier-collection")

#     def test_rating_is_non_negative(self):
#         seller = Sellers(userID = x, sellerName = "Bob's Premier Collection", rating = -1)
#         seller.save()
#         self.assertEqual(seller.views >= 0, True, f"Seller rating should be non negative. Instead rating of {seller.rating} was recieved")

class PopulationScriptTests(TestCase):
    def setUp(self):
    #Import and run the population script
        try:
            import populate_whitemarket
        except ImportError:
            raise ImportError(f"{FAILURE_HEADER} Could not import populate_whitemarket. Check it's in the right location (the first white_market directory){FAILURE_FOOTER}")
        
        if 'populate' not in dir(populate_whitemarket):
            raise NameError(f"{FAILURE_HEADER}The populate() function does not exist in the populate_whitemarket module. This is required{FAILURE_FOOTER}")
        
        #Now call the population script
        populate_whitemarket.populate()
    
    def test_users(self):
        #There should be 2 users
        #CHANGE TEST LATER SO THAT 5 USERS ARE REQUIRED.
        users = Users.objects.filter()
        users_len = len(users)
        users_str = map(str, users)

        self.assertEquals(users_len, 2, f"{FAILURE_HEADER} Expecting 2 users to be created, but found {users_len}.{FAILURE_FOOTER}")
        self.assertTrue('bob' in users_str, f"{FAILURE_HEADER} The user 'bob' was expected but not created.{FAILURE_FOOTER}")
        self.assertTrue('marla' in users_str, f"{FAILURE_HEADER} The user 'marla' was expected but not created.{FAILURE_FOOTER}")
    
    def test_sellers(self):
        #There should be 1 seller
        #CHANGE TEST LATER SO THAT 2 SELLERS ARE REQUIRED.
        sellers = Seller.objects.filter()
        sellers_len = len(sellers)
        sellers_str = map(str, sellers)

        self.assertEquals(sellers_len, 1, f"{FAILURE_HEADER} Expecting 1 seller to be created, but found {sellers_len}.{FAILURE_FOOTER}")
        self.assertTrue('marla' in sellers_str, f"{FAILURE_HEADER} The seller 'marla' was expected but not created.{FAILURE_FOOTER}")
        for seller in sellers:
            try:
                seller_name = seller.users
                Users.objects.get(username = seller_name)
            except Users.DoesNotExist:
                raise ValueError(f"{FAILURE_HEADER} Seller '{seller_name}' does not exist in User table.{FAILURE_FOOTER}")

    def test_stores(self):
        #There should be 1 store
        #CHANGE TEST LATER SO THAT 2 STORES ARE REQUIRED.
        stores = Stores.objects.filter()
        stores_len = len(stores)
        stores_str = map(str, stores)
        excepted_num_stores = 1

        self.assertEquals(stores_len, excepted_num_stores, f"{FAILURE_HEADER} Expecting {excepted_num_stores} store to be created, but found {stores_len}.{FAILURE_FOOTER}")
        self.assertTrue("UMBRA_LLA" in stores_str, f"{FAILURE_HEADER} The store 'UMBRA_LLA' was expected but not created.{FAILURE_FOOTER}")
    
    def test_items(self):
        #There should be 2 items
        #CHANGE TEST LATER SO THAT 3 or 4? ITEMS ARE REQUIRED.
        items = Items.objects.filter()
        items_len = len(items)
        items_str = map(str, items)

        expected_stores = {'UMBRA_LLA': {'umbrella', 'football'}}

        self.assertEquals(items_len, 2, f"{FAILURE_HEADER} Expecting 2 items to be created, but found {items_len}.{FAILURE_FOOTER}")
        self.assertTrue("umbrella" in items_str, f"{FAILURE_HEADER} The item 'umbrella' was expected but not found.{FAILURE_FOOTER}")
        self.assertTrue("football" in items_str, f"{FAILURE_HEADER} The item 'football' was expected but not found.{FAILURE_FOOTER}")

        for expected_store_name in expected_stores:
            expected_store_items = expected_stores[expected_store_name]
            self.check_store_items(expected_store_name, expected_store_items)
    
    def check_store_items(self, expected_store_name, expected_store_items):
        try:
            expected_store = Stores.objects.get(storeName=expected_store_name)
        except Stores.DoesNotExist:
            raise ValueError(f"{FAILURE_HEADER} Expected {expected_store} store, but not created")
        
        actual_items = Items.objects.filter(storename = expected_store)

        #FIRST CHECK WE HAVE THE SAME !!!NUMBER!!! OF ITEMS IN EACH STORE AS EXPECTED
        actual_items_len = len(actual_items)
        expected_items_len = len(expected_store_items)

        self.assertEquals(actual_items_len, expected_items_len)

        #NOW CHECK WE HAVE THE CORRECT ITEMS FOR EACH STORE
        actual_items_names = set(map(str, actual_items))
        self.assertEquals(actual_items_names, expected_store_items, f"expected the following items for the store {expected_store}: {expected_store_items}. But found {actual_items_names}")




