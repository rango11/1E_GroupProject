from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

ratingChoices = [(1,1),(2,2),(3,3),(4,4),(5,5)]

#I left out the tags from stores and items as i'm unsure how to implement 5 different foreign keys user the tagID field

    
class Users(models.Model):
    userID = models.BigAutoField(unique=True,primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    profilePicture = models.ImageField(blank= True)
    description = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Seller(models.Model):
    #userID = models.ForeignKey(Users,on_delete=models.CASCADE,primary_key=True)
    sellerName = models.CharField(max_length=30)
    rating = models.IntegerField(choices=ratingChoices,default=1)#error saying how max length was ignored for integerifeld
    users=models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        verbose_name_plural = 'Sellers'
    def __str__(self):
        return self.sellerName
    
class Stores(models.Model):
    storeID = models.BigAutoField(unique=True,primary_key=True)
    storeName = models.CharField(max_length=30)
    storeDescription = models.CharField(max_length=128)
    class Meta:
        verbose_name_plural = 'Stores'
    def __str__(self):
        return self.storeName   
     
class Tags(models.Model):
    tagID = models.BigAutoField(primary_key=True,unique=True)
    tagName = models.CharField(max_length=30)
    #itemID=models.ForeignKey(Items,on_delete=models.CASCADE)

    shopname=models.ForeignKey(Stores, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Tags'
    def __str__(self):
        return self.tagName

#
class Items(models.Model):
    itemID = models.BigAutoField(unique=True,primary_key=True)
    itemName = models.CharField(max_length=30) #Added this so i can return something with __str__
    sellerName = models.ForeignKey(Seller, on_delete=models.CASCADE)
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    storename=models.ForeignKey(Stores, on_delete=models.CASCADE)
    
    tags=models.ManyToManyField(Tags)
    
    isDigital = models.BooleanField()
    itemDescription = models.CharField(max_length=128)
    itemImage = models.ImageField(blank= True)
    #NEED TO ADD RESTRICTED CHOICE FOR ALL CONDITIONS:
    condition = models.CharField(max_length=10)
    listedTime = models.DateTimeField()
    sellTime = models.DateTimeField()
    buyNowPrice = models.FloatField(max_length=100, default=0.0)
    class Meta:
        verbose_name_plural = 'Items'
    def __str__(self):
        return self.itemName





class Bids(models.Model):
    bidID = models.BigAutoField(unique=True,primary_key=True)
    itemID = models.ForeignKey(Items,on_delete=models.CASCADE)
    userID = models.ForeignKey(Users,on_delete=models.CASCADE)
    bidTime = models.DateTimeField()
    bidPrice = models.FloatField(max_length=100, default=0.0)
    class Meta:
        verbose_name_plural = 'Bids'
    def __str__(self):
        return self.bidID


