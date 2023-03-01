from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

ratingChoices = [(1,1),(2,2),(3,3),(4,4),(5,5)]

#I left out the tags from stores and items as i'm unsure how to implement 5 different foreign keys user the tagID field

class Users:
    userID = models.BigAuto(unique=True,primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    profilePicture = models.ImageField()
    description = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.username


class Items:
    itemID = models.BigAuto(unique=True,primary_key=True)
    itemName = models.CharField(max_length=30) #Added this so i can return something with __str__
    sellerID = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    sellerName = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    isDigital = models.BooleanField()
    itemDescription = models.CharField(max_length=128)
    itemImage = models.ImageField()
    #NEED TO ADD RESTRICTED CHOICE FOR ALL CONDITIONS:
    condition = models.CharField(max_length=10)
    listedTime = models.DateTime()
    sellTime = models.DateTime()
    buyNowPrice = models.DecimalField()

    def __str__(self):
        return self.itemName


class Seller:
    userID = models.ForeignKey(Users,on_delete=models.CASCADE,primary_key=True)
    sellerName = models.CharField(max_length=30)
    rating = models.IntegerField(max_length=1,choices=ratingChoices,default=1)

    def __str__(self):
        return self.sellerName

class Tags:
    tagID = models.AutoField(primary_key=true,unique=true)
    tagName = models.CharField(max_length=30)

    def __str__(self):
        return self.tagName


class Bids:
    bidID = models.BigAuto(unique=true,primary_key=true)
    itemID = models.ForeignKey(Items,on_delete=models.CASCADE)
    userID = models.ForeignKey(Users,on_delete=models.CASCADE)
    bidTime = models.DateTime()
    bidPrice = models.DecimalField()

    def __str__(self):
        return self.bidID

class Stores:
    storeID = models.BigAuto(unique=true,primary_key=true)
    storeName = models.charField(max_length=30)
    storeDescription = models.CharField(max_length=128)

    def __str__(self):
        return self.storeName


