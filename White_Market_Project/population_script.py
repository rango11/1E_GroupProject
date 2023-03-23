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
 # First, we will create lists of dictionaries containing the pages
 # we want to add into each category.
 # Then we will create a dictionary of dictionaries for our categories.
 # This might seem a little bit confusing, but it allows us to iterate
 # through each data structure, and add the data to our models.

    #usr1=Users(1,"bob","absdefg",None,"","bob@gmail.com","01234234234")
    #usr2=Users(2,"marla","hijkmlm",None,"","marla@gmail.com","12310931231")
    #users = [usr1,usr2]


    # Using readlines()
    namefile = open('names.txt', 'r')
    nLines = namefile.readlines()
    passfile = open('passwords.txt', 'r')
    PLines = passfile.readlines()
    emailfile = open('emails.txt', 'r')
    ELines = emailfile.readlines()
    phonefile = open('phoneN.txt', 'r')
    phoneLines = phonefile.readlines()
    # brandfile = open('brands.txt', 'r')
    # brandLines = brandfile.readlines()

    users=[]
    userProfiles = []
    sellers=[]
    stores=[]
    items=[]
    tagsA=[]
      
    for counter in range(len(nLines)):
        # print("£££££££££££££££££££££££££££££££££££££££££££")
        # print(nLines[counter])
        # print("££££££££££££££££££££££££££££££££££££££££££")
        # if (nLines[counter] == "" or nLines[counter] == None):
        #     print("We have a bad value")
        new_user=User.objects.get_or_create(username=nLines[counter],password=PLines[counter])[0]
        new_user.email = ELines[counter]
        new_user.save()
        users.append(new_user)

        new_user_profile = UserProfile.objects.get_or_create(user = new_user,
                                                            profilePicture=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                            description="",
                                                            phoneNo=phoneLines[counter])[0]
        new_user_profile.save()
        # print("£££££££££££££££££££££££££££££££££££££££££")
        # print(new_user_profile)
        # print("£££££££££££££££££££££££££££££££££££££££££")
        userProfiles.append(new_user_profile)

    for counter in range(8):
        seller=Sellers.objects.get_or_create(userID =userProfiles[counter],
                                             sellerName=nLines[counter],
                                             rating=random.randint(1,5))[0]
        seller.save()
        # print("£££££££££££££££££££££££££££££££££££££££££")
        # print(seller)
        # print("£££££££££££££££££££££££££££££££££££££££££")
        sellers.append(seller)

   
    #a store to make use of
    store=Stores.objects.get_or_create(storeName="Baseball Collection",storeDescription="Everything you need baseball related whether digital or physical")[0]
    store.save()
    storeT=Stores.objects.get_or_create(storeName="Rocket League Market",storeDescription="Rocket League skins at the most competitive prices" )[0]
    storeT.save()
    storeC=Stores.objects.get_or_create(storeName="Pokemon",storeDescription="Everyone loves Pokemon" )[0]
    storeC.save()
    storeV=Stores.objects.get_or_create(storeName="Books",storeDescription="Rare fictional and non-fictional books." )[0]
    storeV.save()
    storeB=Stores.objects.get_or_create(storeName="Oddities",storeDescription="Obscure items that you won't find anywhere else." )[0]
    storeB.save()
    stores.append(store)
    stores.append(storeT)
    stores.append(storeC)
    stores.append(storeV)
    stores.append(storeB)

    date_modified =timezone.now()#datetime.date.today() #models.DateTimeField(auto_now_add=True)#the current time apparently? just to fill the dates
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
