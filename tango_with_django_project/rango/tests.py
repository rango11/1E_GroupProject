import os
import warnings
import importlib
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Users, Sellers, Stores, Items
from django.core.exceptions import ObjectDoesNotExist

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==============={os.linesep}TEST FAILURE = ({os.linesep}==============={os.linesep})"
FAILURE_FOOTER = f"{os.linesep}"

class SellerMethodTests(TestCase):
    def test_slug_line_creation(self):
        seller = Sellers(userID = x, sellerName = "Bob's Premier Collection", rating = 2)
        seller.save()

        self.assertEqual(seller.slug, "bob's-premier-collection")

    def test_rating_is_non_negative(self):
        seller = Sellers(userID = x, sellerName = "Bob's Premier Collection", rating = -1)
        seller.save()
        self.assertEqual(seller.views >= 0, True, f"Seller rating should be non negative. Instead rating of {seller.rating} was recieved")

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
        sellers = Sellers.objects.filter()
        sellers_len = len(sellers)
        sellers_str = map(str, sellers)

        self.assertEquals(sellers_len, 1, f"{FAILURE_HEADER} Expecting 1 seller to be created, but found {sellers_len}.{FAILURE_FOOTER}")
        self.assertTrue('marla' in sellers_str, f"{FAILURE_HEADER} The seller 'marla' was expected but not created.{FAILURE_FOOTER}")
        for seller in sellers:
            try:
                Users.objects.get(seller.users)
            except ObjectDoesNotExist:
                raise ValueError(f"{FAILURE_HEADER} Seller does not exist in User table.{FAILURE_FOOTER}")
                #NOT SURE IF THIS LINE ^ WORKS.

    def test_stores(self):
        #There should be 1 store
        #CHANGE TEST LATER SO THAT 2 STORES ARE REQUIRED.
        stores = Stores.objects.filter()
        stores_len = len(stores)
        stores_str = map(str, stores)

        self.assertEquals(stores_len, 1, f"{FAILURE_HEADER} Expecting 1 store to be created, but found {stores_len}.{FAILURE_FOOTER}")
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

        for expected_store in expected_stores:
            store_items = expected_stores[expected_store]
            self.check_store_items(expected_store, store_items)
    
    def check_store_items(self, expected_store, store_items):
        store = Stores.objects.get(name=expected_store)
        items = Items.objects.filter(name=store_items)

        #FIRST CHECK WE HAVE THE SAME !!!NUMBER!!! OF ITEMS IN EACH STORE AS EXPECTED
        items_len = len(items)
        store_items_len = len(store_items)

        self.assertEquals(items_len, store_items_len, f"{FAILURE_HEADER} Expected {store_items_len} items in {len(store)}, but found {items_len}.{FAILURE_FOOTER}")

        #NOW CHECK WE HAVE THE CORRECT ITEMS FOR EACH STORE
        for expected_item in store_items:
            try:
                item = Items.objects.get(expected_item)
            except ObjectDoesNotExist:
                raise ValueError(f"{FAILURE_HEADER}The item {expected_item} in the {store} was not found")
            
            self.assertEquals(item.storename, store)




