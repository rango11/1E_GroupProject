import os
import warnings
import importlib
import tempfile

from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import fields as django_fields
#from populate_whitemarket import populate
from WhiteMarket import forms
from WhiteMarket.models import *

#from django.core.exceptions import ObjectDoesNotExist

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==============={os.linesep}TEST FAILURE = ({os.linesep}==============={os.linesep})"
FAILURE_FOOTER = f"{os.linesep}"

"""
Below are some helper functions to create objects of the models.
"""

def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

def create_userProfile_object():
    user_object = create_user_object()
    user_profile = UserProfile.objects.get_or_create(user = user_object,
                                                                profilePicture = tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                                description = 'test user profile object',
                                                                phoneNo = '07345678934')[0]
    user_profile.save()
    return user_profile

def create_seller_object():
    user_profile = create_userProfile_object()
    seller_object = Sellers.objects.get_or_create(userID = user_profile, 
                                           sellerName = 'test_seller',
                                           rating = 2)[0]
    seller_object.save()
    return seller_object

def create_store_object():
    store_object = Stores.objects.get_or_create(storeName = 'Baseball cards', 
                                                storeDescription = 'All the baseball cards your heart desires')[0]
    store_object.save()
    return store_object



# class SellerTests(TestCase):
#     def test_slug_line_creation(self):
#         seller = Sellers.objects.get_or_create(userID=x)
#         seller.sellerName = "Bob's premier collection"
#         seller.save()

#         self.assertEqual(seller.slug, "bob's-premier-collection")

#     def test_rating_is_non_negative(self):
#         seller = Sellers(userID = x, sellerName = "Bob's Premier Collection", rating = -1)
#         seller.save()
#         self.assertEqual(seller.views >= 0, True, f"Seller rating should be non negative. Instead rating of {seller.rating} was recieved")

class RegistrationTests(TestCase):
    def test_registration_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''
        try:
            url = reverse('whitemarket:register')
        except NoReverseMatch:
            self.assertTrue(False, f"{FAILURE_HEADER}Check that app name in url.py is 'whitemarket'{FAILURE_FOOTER}")
        else:
            self.assertEquals(url, '/whitemarket/register/', f"{FAILURE_HEADER}Have you created the whitemarket:register URL mappign correctly? It should point to the register view")
    
    def test_registration_template(self):
        """
        Does the register.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'WhiteMarket')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'register.html' template in the 'templates/WhiteMarket/' directory. Did you put it in the right place?{FAILURE_FOOTER}")
    
    def test_registration_get_response(self):
        """
        Checks the GET response of the registration view. Is the form enctype="multipart/form-data".
        """
        request = self.client.get(reverse('whitemarket:register'))
        content = request.content.decode('utf-8')
        self.assertTrue('enctype="multipart/form-data"' in content, f"{FAILURE_HEADER}The form should use 'enctype' = 'multipart/form-data'{FAILURE_FOOTER}")

    def test_bad_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        What if we submit a blank form?
        """
        request = self.client.post(reverse('whitemarket:register'))
        content = request.content.decode('utf-8')
        self.assertTrue('<ul class="errorlist">' in content)
    
    def test_good_form_creation(self):
        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'} ##THIS IS FOR THE USER MODEL MADE BY DJANGO
        user_form = forms.UserForm(data=user_data)
        profile_data = {'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name, 'description': "I love baseball cards!", 'phoneNo':'07225652981'}
        profile_form = forms.UserProfileForm(data=profile_data)  ##THIS IS FOR OUR UserProfile MODEL

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm  was not valid after entering the required data. {FAILURE_FOOTER}")
        self.assertTrue(profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data.{FAILURE_FOOTER}")

        user_object = user_form.save()   
        user_object.set_password(user_data['password'])
        user_object.save()

        profile_object = profile_form.save(commit=False)  #THIS IS A USER IN OUR USERS MODEL 
        profile_object.user = user_object
        profile_object.save()

        self.assertEquals(len(User.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a (Django) User object created, but it didn't appear. Check your UserForm implementation, and try again.{FAILURE_FOOTER}")
        self.assertEquals(len(UserProfile.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a UserProfile object created, but it didn't appear. Check your UserProfileForm implementation, and try again.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}We couldn't log our sample user in during the tests. Please check your implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")

    def test_good_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        We should be able to log a user in with new details after this!
        """
        post_data = {'username': 'qwerty', 'password': 'test123', 'email': 'test@test.com', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name, 'description': "I love baseball cards!", 'phoneNo':'07225652981'}
        request = self.client.post(reverse('whitemarket:register'), post_data)
        content = request.content.decode('utf-8')
        self.assertTrue(self.client.login(username='qwerty', password='test123'), f"{FAILURE_HEADER}We couldn't log in the user we created using your registration form. Please check your implementation of the register() view. Are you missing a .save() call?{FAILURE_FOOTER}")

class LoginTests(TestCase):
    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('whitemarket:login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")
    
    def test_login_template(self):
        """
        Does the login.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'whitemarket')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/whitemarket/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

class LogoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. Does it work? Does it actually log you out?
    """
    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in.
        This should according to the book redirect you to the login page.
        """
        response = self.client.get(reverse('whitemarket:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('whitemarket:login'))

    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('whitemarket:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Please check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")

class SellerTests(TestCase):
    def test_create_seller_form(self):
        seller_form = forms.SellerForm(data={'sellerName':'test_seller'})
        self.assertTrue(seller_form.is_valid(), f"{FAILURE_HEADER} The SellerForm should be valid but it was not. Check SellerForm implementation")

        seller_object = seller_form.save(commit=False)
        temp_user_profile = create_userProfile_object()
        seller_object.userID = UserProfile.objects.get(userID =temp_user_profile.userID)
        seller_object.save()
        self.assertTrue(len(Sellers.objects.all()) != 0, f"{FAILURE_HEADER} Seller object was not created.{FAILURE_FOOTER}")

    def test_list_item_form(self):
        item_store = create_store_object()
        item_data = {'itemName': 'Babe Ruth baseball card', 'isDigital': False, 'itemDescription': 'Famous baseball card',
                    'storeID': item_store.storeID, 'condition': 'Used',  'buyNowPrice':100, 'itemImage': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        item_form = forms.ItemForm(data=item_data)

        self.assertTrue(item_form.is_valid(), f"{FAILURE_HEADER}The ItemForm should be valid but it was not. Check ItemForm implementation.{FAILURE_FOOTER}")


   

# class UserTests(TestCase):
#     def test_sign_up_form(self):
#         self.client.post(reverse('rango:sign_up'), {'name': 'bob', 'password': 'qwerTyuio5p', 'description': "I love baseball cards!", 'phoneNo':'07225652981'})
#         bob = Users.objects.filter(username='bob')
#         self.assertEquals(len(bob), 1, f"{FAILURE_HEADER} When adding a new user by the sign up form, it does not appear in the list of Users. {FAILURE_FOOTER}")


#     def test_sign_in_form(self):
#         user_object = create_user_object()
#         response = self.client.post(reverse('rango:login'), {'username': 'testuser', 'password': 'testabc123'})
        
#         try:
#             self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
#         except KeyError:
#             self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

#     def test_good_form_creation(self):
#         USER_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'} ##THIS IS FOR THE USER MODEL MADE BY DJANGO
#         USER_form = forms.USERForm(data=USER_data)

#         users_data = {'description': "I love baseball cards!", 'phoneNo':'07225652981', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
#         users_form = forms.UserForm(data=users_data)  ##THIS IS FOR OUR USERS MODEL

#         self.assertTrue(USER_form.is_valid(), f"{FAILURE_HEADER}The USERForm (Django User) was not valid after entering the required data. {FAILURE_FOOTER}")
#         self.assertTrue(users_form.is_valid(), f"{FAILURE_HEADER}The UsersForm (WhiteMarket user) was not valid after entering the required data.{FAILURE_FOOTER}")

#         USER_object = USER_form.save()    #AGAIN THIS IS A USER IN THE DJANGO USER MODEL
#         USER_object.set_password(USER_data['password'])
#         USER_object.save()
        
#         users_object = users_form.save(commit=False)  #THIS IS A USER IN OUR USERS MODEL 
#         users_object.user = users_object
#         users_object.save()
        
#         self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a (Django) User object created, but it didn't appear. Check your UserForm implementation, and try again.{FAILURE_FOOTER}")
#         self.assertEqual(len(whitemarket.models.Users.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a (WhiteMarket) Users object created, but it didn't appear. Check your UserProfileForm implementation, and try again.{FAILURE_FOOTER}")
#         self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}We couldn't log our sample user in during the tests. Please check your implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")


# class PopulationScriptTests(TestCase):
#     def setUp(self):
#     #Import and run the population script
#         try:
#             import populate_whitemarket
#         except ImportError:
#             raise ImportError(f"{FAILURE_HEADER} Could not import populate_whitemarket. Check it's in the right location (the first white_market directory){FAILURE_FOOTER}")
        
#         if 'populate' not in dir(populate_whitemarket):
#             raise NameError(f"{FAILURE_HEADER}The populate() function does not exist in the populate_whitemarket module. This is required{FAILURE_FOOTER}")
        
#         #Now call the population script
#         populate_whitemarket.populate()
    
#     def test_users(self):
#         #There should be 2 users
#         #CHANGE TEST LATER SO THAT 5 USERS ARE REQUIRED.
#         users = Users.objects.filter()
#         users_len = len(users)
#         users_str = map(str, users)

#         self.assertEquals(users_len, 2, f"{FAILURE_HEADER} Expecting 2 users to be created, but found {users_len}.{FAILURE_FOOTER}")
#         self.assertTrue('bob' in users_str, f"{FAILURE_HEADER} The user 'bob' was expected but not created.{FAILURE_FOOTER}")
#         self.assertTrue('marla' in users_str, f"{FAILURE_HEADER} The user 'marla' was expected but not created.{FAILURE_FOOTER}")
    
#     def test_sellers(self):
#         #There should be 1 seller
#         #CHANGE TEST LATER SO THAT 2 SELLERS ARE REQUIRED.
#         sellers = Sellers.objects.filter()
#         sellers_len = len(sellers)
#         sellers_str = map(str, sellers)

#         self.assertEquals(sellers_len, 1, f"{FAILURE_HEADER} Expecting 1 seller to be created, but found {sellers_len}.{FAILURE_FOOTER}")
#         self.assertTrue('marla' in sellers_str, f"{FAILURE_HEADER} The seller 'marla' was expected but not created.{FAILURE_FOOTER}")
#         for seller in sellers:
#             try:
#                 seller_name = seller.users
#                 Users.objects.get(username = seller_name)
#             except Users.DoesNotExist:
#                 raise ValueError(f"{FAILURE_HEADER} Seller '{seller_name}' does not exist in User table.{FAILURE_FOOTER}")

#     def test_stores(self):
#         #There should be 1 store
#         #CHANGE TEST LATER SO THAT 2 STORES ARE REQUIRED.
#         stores = Stores.objects.filter()
#         stores_len = len(stores)
#         stores_str = map(str, stores)
#         excepted_num_stores = 1

#         self.assertEquals(stores_len, excepted_num_stores, f"{FAILURE_HEADER} Expecting {excepted_num_stores} store to be created, but found {stores_len}.{FAILURE_FOOTER}")
#         self.assertTrue("UMBRA_LLA" in stores_str, f"{FAILURE_HEADER} The store 'UMBRA_LLA' was expected but not created.{FAILURE_FOOTER}")
    
#     def test_items(self):
#         #There should be 2 items
#         #CHANGE TEST LATER SO THAT 3 or 4? ITEMS ARE REQUIRED.
#         items = Items.objects.filter()
#         items_len = len(items)
#         items_str = map(str, items)

#         expected_stores = {'UMBRA_LLA': {'umbrella', 'football'}}

#         self.assertEquals(items_len, 2, f"{FAILURE_HEADER} Expecting 2 items to be created, but found {items_len}.{FAILURE_FOOTER}")
#         self.assertTrue("umbrella" in items_str, f"{FAILURE_HEADER} The item 'umbrella' was expected but not found.{FAILURE_FOOTER}")
#         self.assertTrue("football" in items_str, f"{FAILURE_HEADER} The item 'football' was expected but not found.{FAILURE_FOOTER}")

#         for expected_store_name in expected_stores:
#             expected_store_items = expected_stores[expected_store_name]
#             self.check_store_items(expected_store_name, expected_store_items)
    
#     def check_store_items(self, expected_store_name, expected_store_items):
#         try:
#             expected_store = Stores.objects.get(storeName=expected_store_name)
#         except Stores.DoesNotExist:
#             raise ValueError(f"{FAILURE_HEADER} Expected {expected_store} store, but not created")
        
#         actual_items = Items.objects.filter(storename = expected_store)

#         #FIRST CHECK WE HAVE THE SAME !!!NUMBER!!! OF ITEMS IN EACH STORE AS EXPECTED
#         actual_items_len = len(actual_items)
#         expected_items_len = len(expected_store_items)

#         self.assertEquals(actual_items_len, expected_items_len)

#         #NOW CHECK WE HAVE THE CORRECT ITEMS FOR EACH STORE
#         actual_items_names = set(map(str, actual_items))
#         self.assertEquals(actual_items_names, expected_store_items, f"expected the following items for the store {expected_store}: {expected_store_items}. But found {actual_items_names}")


# class TemplateTests(TestCase):
#     populate()
#     def test_transactionComplete_template(self):
#         response = self.client.get(reverse('rango:transactionComplete'))
#         self.assertTemplateUsed(response, 'rango/base.html', f"{FAILURE_HEADER}The transactionComplete.html template is not used for the add_category() view. The specification requires this.{FAILURE_FOOTER}")





