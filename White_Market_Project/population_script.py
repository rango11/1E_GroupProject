import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','White_Market_Project.settings')

import django
from django.db import models
django.setup()
from WhiteMarket.models import *
import datetime
import tempfile
from django.utils import timezone
import pytz


def populate():
    namefile = open('names.txt', 'r')
    nLines = namefile.readlines()
    passfile = open('passwords.txt', 'r')
    PLines = passfile.readlines()
    emailfile = open('emails.txt', 'r')
    ELines = emailfile.readlines()
    phonefile = open('phoneN.txt', 'r')
    phoneLines = phonefile.readlines()
    users, userProfiles, sellers, stores, items=[]
      
    for counter in range(len(nLines)):
        new_user=User.objects.get_or_create(username=nLines[counter],password=PLines[counter])[0]
        new_user.email = ELines[counter]
        new_user.save()
        users.append(new_user)

        new_user_profile = UserProfile.objects.get_or_create(user = new_user,
                                                             profilePicture=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                             description="",
                                                             phoneNo=phoneLines[counter])[0]
        new_user_profile.save()
        userProfiles.append(new_user_profile)

    #Create 8 sellers
    for counter in range(8):
        seller=Sellers.objects.get_or_create(userID =userProfiles[counter],
                                             sellerName=nLines[counter],
                                             rating=random.randint(1,5))[0]
        seller.save()
        sellers.append(seller)

   
    store1=Stores.objects.get_or_create(storeName="Baseball Collection",storeDescription="Everything you need baseball related whether digital or physical")[0]
    store1.save()
    store2=Stores.objects.get_or_create(storeName="Rocket League Market",storeDescription="Rocket League skins at the most competitive prices" )[0]
    store2.save()
    store3=Stores.objects.get_or_create(storeName="Pokemon",storeDescription="Everyone loves Pokemon" )[0]
    store3.save()
    store4=Stores.objects.get_or_create(storeName="Books",storeDescription="Rare fictional and non-fictional books." )[0]
    store4.save()
    store5=Stores.objects.get_or_create(storeName="Oddities",storeDescription="Obscure items that you won't find anywhere else." )[0]
    store5.save()
    stores.append(store1)
    stores.append(store2)
    stores.append(store3)
    stores.append(store4)
    stores.append(store5)

    #Create 5 items for each store
    is_digital = random.choice([True,False])
    for store in stores:
        for counter in range(5):
            if store.storeName == "Rocket League Market":
                is_digital = True
            randomSeller = random.randint(0,len(sellers)-1)
            item=Items.objects.get_or_create(itemName= f"{store.storeName} item {counter}", 
                                            sellerID=sellers[randomSeller],
                                            sellerName = sellers[randomSeller].sellerName,
                                            storeID= store,
                                            isDigital= is_digital, 
                                            itemDescription="...",
                                            itemImage=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                            condition='New', 
                                            buyNowPrice=random.randint(10,200))[0]
            item.save()
            items.append(item)

    date_modified =timezone.now()#datetime.date.today() #models.DateTimeField(auto_now_add=True)#the current time apparently? just to fill the dates
    #Create 15 bids
    for counter in range(15):
        bid=Bids.objects.get_or_create(itemID=items[random.randint(0, len(items)-1)],
                                       userID=userProfiles[random.randint(0, len(userProfiles)-1)],
                                       bidTime=date_modified,
                                       bidPrice=random.randint(0,100))[0]
        bid.save()

    
    
# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
