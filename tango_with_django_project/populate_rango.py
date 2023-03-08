import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
from django.db import models
django.setup()
from rango.models import Users, Sellers,Stores, Items, Tags, Bids
import datetime
from django.utils import timezone
import pytz


def populate():
 # First, we will create lists of dictionaries containing the pages
 # we want to add into each category.
 # Then we will create a dictionary of dictionaries for our categories.
 # This might seem a little bit confusing, but it allows us to iterate
 # through each data structure, and add the data to our models.

    #usr1=Users(1,"bob","absdefg",None,"","bob@gmail.com","01234234234")
    #usr2=Users(2,"marla","hijkmlm",None,"","marla@gmail.com","12310931231")
    #users = [usr1,usr2]

    #users 1 wont be a seller, user 2 will be a seller
    usr1=Users.objects.get_or_create(username="bob",password="absdefg",profilePicture=None,description="",email="bob@gmail.com",phoneNo="01234234234")[0]
    usr1.save()
    usr2=Users.objects.get_or_create(username="marla",password="hijkmlm",profilePicture=None,description="aa",email="marla@gmail.com",phoneNo="12310931231")[0]
    usr2.save()

    seller=Sellers.objects.get_or_create(sellerName="marla",rating=3,users=usr2)[0]
    seller.save()
    #a store to make use of
    store=Stores.objects.get_or_create(storeName="UMBRA_LLA",storeDescription="" )[0]
    store.save()

    # an item for multiple bids, multiple items for a shop
    date_modified =timezone.now()#datetime.date.today() #models.DateTimeField(auto_now_add=True)#the current time apparently? just to fill the dates
    item1=Items.objects.get_or_create(itemName="umbrella", 
                                sellerName=seller,username=usr2,
                                storename=store,isDigital=False, 
                                itemDescription="protects from rain innit",itemImage=None,
                                condition="good", listedTime=date_modified,
                                sellTime=date_modified, buyNowPrice=100.0
                                )[0]
    item1.save()
    item2=Items.objects.get_or_create(itemName="football", 
                                sellerName=seller,username=usr2,
                                storename=store,isDigital=False, 
                                itemDescription="is a football",itemImage=None,
                                condition="excellent", listedTime=date_modified,
                                sellTime=date_modified, buyNowPrice=10.0
                                )[0]
    item2.save()

    b1=Bids.objects.get_or_create(itemID=item1,userID=usr1,bidTime=date_modified,bidPrice=10)[0]
    b1.save()
    b2=Bids.objects.get_or_create(itemID=item1,userID=usr1,bidTime=date_modified,bidPrice=40)[0]
    b2.save()

    t1=Tags.objects.get_or_create(tagName="BigBrand",shopname=store)[0]
    t1.save()
    t2=Tags.objects.get_or_create(tagName="OnSale",shopname=store)[0]
    t2.save()

    #t3=Tags(tagName="BigBrand",shopname=store)
    #t4=Tags(tagName="OnSale",shopname=store)
    #t3.save()
    #t4.save()

    item1.tags.add(t1)
    item1.tags.add(t2)

    #item2.tags.add(t1)
    
    
# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
