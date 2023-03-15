from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

ratingChoices = [(1,1),(2,2),(3,3),(4,4),(5,5)]
tagRecords = Tags.objects.all()
tagNameList = []

for tags.tagName in tagRecords:
    tagNameList.append(tags.tagName)

class Users(models.Model):

    #commented fields appear in User model

    user = models.OneToOneField(User, on_delete=models.CASCADE) #Links to User model to allow user authentication functionality

    userID = models.BigAutoField(unique=True,primary_key=True)
    #username = models.CharField(max_length=30)
    #password = models.CharField(max_length=32)
    profilePicture = models.ImageField(upload_to='profile_images', blank=True)
    description = models.CharField(max_length=128)
    #email = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Users, self).save(*args, **kwargs)

class Sellers(models.Model):
    userID = models.OneToOneField("Users",on_delete=models.CASCADE,primary_key=True)
    sellerName = models.CharField(max_length=30)
    rating = models.IntegerField(choices=ratingChoices,default=1)

    def __str__(self):
        return self.sellerName

class Tags(models.Model):
    tagID = models.AutoField(primary_key=True,unique=True)
    tagName = models.CharField(max_length=30)



class Bids(models.Model):
    bidID = models.BigAutoField(unique=True,primary_key=True)
    itemID = models.ForeignKey("Items",on_delete=models.CASCADE)
    userID = models.ForeignKey("Users",on_delete=models.CASCADE)
    bidTime = models.DateTimeField()
    bidPrice = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return self.bidID

class Stores(models.Model):
    storeID = models.BigAutoField(unique=True,primary_key=True)
    storeName = models.CharField(max_length=30)
    storeDescription = models.CharField(max_length=128)
    #storeTag1 = models.AutoField() #Cant have them as foreign keys to Tags
    #storeTag2 = models.AutoField()
    #storeTag3 = models.AutoField()
    #storeTag4 = models.AutoField()
    #storeTag5 = models.AutoField()
    tag = models.CharField(choices=tagNameList)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.storeName)
        super(Stores, self).save(*args, **kwargs)

    def __str__(self):
        return self.storeName


class Items(models.Model):
    itemID = models.BigAutoField(unique=True,primary_key=True)
    itemName = models.CharField(max_length=30) #Added this so i can return something with __str__
    sellerID = models.ForeignKey("Sellers", on_delete=models.CASCADE,related_name="sellerID")
    userID = models.ForeignKey("Users", on_delete=models.CASCADE,related_name="itemUserID")
    sellerName = models.ForeignKey("Sellers", on_delete=models.CASCADE,related_name="itemSellerName")
    username = models.ForeignKey("Users", on_delete=models.CASCADE,related_name="username")
    isDigital = models.BooleanField()
    itemDescription = models.CharField(max_length=128)
    itemImage = models.ImageField()
    #NEED TO ADD RESTRICTED CHOICE FOR ALL CONDITIONS:
    condition = models.CharField(max_length=10)
    listedTime = models.DateTimeField()
    sellTime = models.DateTimeField()
    buyNowPrice = models.DecimalField(decimal_places=2,max_digits=10)
    tag = models.CharField(choices=tagNameList)
    #otherTag1 = models.AutoField() #Cant be foreign key to tags, only store
    #otherTag2 = models.AutoField()
    #otherTag3 = models.AutoField()
    #otherTag4 = models.AutoField()
    #otherTag5 = models.AutoField()
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.itemName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.itemName)
        super(Items, self).save(*args, **kwargs)