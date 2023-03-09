from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

ratingChoices = [(1,1),(2,2),(3,3),(4,4),(5,5)]

class Users:

    #commented fields appear in User model

    user = models.OneToOneField(User, on_delete=models.CASCADE) #Links to User model to allow user authentication functionality

    userID = models.BigAutoField(unique=True,primary_key=True)
    #username = models.CharField(max_length=30)
    #password = models.CharField(max_length=32)
    profilePicture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.CharField(max_length=128)
    #email = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Users, self).save(*args, **kwargs)

class Sellers:
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
    bidID = models.BigAutoField(unique=true,primary_key=true)
    itemID = models.ForeignKey(Items,on_delete=models.CASCADE)
    userID = models.ForeignKey(Users,on_delete=models.CASCADE)
    bidTime = models.DateTime()
    bidPrice = models.DecimalField()

    def __str__(self):
        return self.bidID

class Stores:
    storeID = models.BigAutoField(unique=true,primary_key=true)
    storeName = models.charField(max_length=30)
    storeDescription = models.CharField(max_length=128)
    storeTag1 = models.AutoField() #Cant have them as foreign keys to Tags
    storeTag2 = models.AutoField()
    storeTag3 = models.AutoField()
    storeTag4 = models.AutoField()
    storeTag5 = models.AutoField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.storeName)
        super(Stores, self).save(*args, **kwargs)

    def __str__(self):
        return self.storeName


class Items:
    itemID = models.BigAutoField(unique=True,primary_key=True)
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
    otherTag1 = models.AutoField() #Cant be foreign key to tags, only store
    otherTag2 = mdoels.AutoField()
    otherTag3 = models.AutoField()
    otherTag4 = models.AutoField()
    otherTag5 = models.AutoField()
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.itemName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.itemName)
        super(Items, self).save(*args, **kwargs)