from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

ratingChoices = [(1,1),(2,2),(3,3),(4,4),(5,5)]

#I left out the tags from stores and items as i'm unsure how to implement 5 different foreign keys user the tagID field

class UserAccount(models.Model):
    # userID = models.BigAuto(unique=True,primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    # username = models.CharField(max_length=30)
    #password = models.CharField(max_length=32)
    profilePicture = models.ImageField()
    description = models.CharField(max_length=128)
    # email = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.user.username



class Sellers(models.Model):
    userID = models.OneToOneField(UserAccount,on_delete=models.CASCADE,unique=True, primary_key=True)
    sellerName = models.CharField(max_length=30)
    rating = models.IntegerField(choices=ratingChoices,default=1)

    def __str__(self):
        return self.sellerName


class Tags(models.Model):
    tagID = models.AutoField(primary_key=True,unique=True)
    tagName = models.CharField(max_length=30)

    def __str__(self):
        return self.tagName



class Stores(models.Model):
    # storeID = models.BigAuto(unique=true,primary_key=true)
    storeName = models.CharField(max_length=30)
    storeDescription = models.CharField(max_length=128)

    def __str__(self):
        return self.storeName
    
class Items(models.Model):
    # itemID = models.BigAuto(unique=True,primary_key=True)
    itemName = models.CharField(max_length=30) #Added this so i can return something with __str__
    sellerID = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    userID = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    #sellerName = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    #username = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    isDigital = models.BooleanField()
    itemDescription = models.CharField(max_length=128)
    itemImage = models.ImageField()
    #NEED TO ADD RESTRICTED CHOICE FOR ALL CONDITIONS:
    condition = models.CharField(max_length=10)
    listedTime = models.DateTimeField()
    sellTime = models.DateTimeField()
    buyNowPrice = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.itemName
    
    
class Bids(models.Model):
    # bidID = models.BigAuto(unique=true,primary_key=true)
    itemID = models.ForeignKey(Items,on_delete=models.CASCADE)
    userID = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    bidTime = models.DateTimeField()
    bidPrice = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.bidID




# from django.db import models
# from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User

# class Category(models.Model):
#     NAME_MAX_LENGTH = 128

#     name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
#     views = models.IntegerField(default=0)
#     likes = models.IntegerField(default=0)
#     slug = models.SlugField(unique=True)

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Category, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name_plural = 'Categories'

#     def __str__(self):
#         return self.name

# class Page(models.Model):
#     TITLE_MAX_LENGTH = 128
#     URL_MAX_LENGTH = 200

#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     title = models.CharField(max_length=TITLE_MAX_LENGTH)
#     url = models.URLField()
#     views = models.IntegerField(default=0)

#     def __str__(self):
#         return self.title

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     website = models.URLField(blank=True)
#     picture = models.ImageField(upload_to='profile_images', blank=True)

#     def __str__(self):
#         return self.user.username

# to do!!!!!!!!!!!!!!!!!!!!!!
    # def save(self, *args, **kwargs):
    #     self.<insert_slug_here> = (slugify(self.<more stuff here>))
    #     super( stuff here, self).save(*args, **kwargs)