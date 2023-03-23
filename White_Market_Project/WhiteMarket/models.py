from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

ratingChoices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
CONDITION_CHOICES = [
    ('new', 'New'),
    ('used', 'Used'),
    ('refurbished', 'Refurbished'), ]


class UserProfile(models.Model):
    # commented fields appear in User model
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)  # Links to User model to allow user authentication
    # functionality

    userID = models.BigAutoField(unique=True, primary_key=True)
    profilePicture = models.ImageField(upload_to='user_profile_photos/', blank=True)
    description = models.CharField(max_length=128)
    phoneNo = models.CharField(max_length=11)

    class Meta:
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)


class Sellers(models.Model):
    sellerID = models.AutoField(primary_key=True)
    userID = models.OneToOneField("UserProfile", on_delete=models.CASCADE)
    sellerName = models.CharField(max_length=30)
    rating = models.IntegerField(choices=ratingChoices, default=1)

    class Meta:
        verbose_name_plural = 'Sellers'

    def __str__(self):
        return self.sellerName


class Bids(models.Model):
    bidID = models.AutoField(unique=True, primary_key=True)
    itemID = models.ForeignKey("Items", on_delete=models.CASCADE)
    userID = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    bidTime = models.DateTimeField()
    bidPrice = models.DecimalField(decimal_places=2, max_digits=10)
    complete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Bids'

    # def __str__(self):
    # return self.bidID


class Stores(models.Model):
    storeID = models.BigAutoField(unique=True, primary_key=True)
    storeName = models.CharField(max_length=30)
    storeDescription = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Stores'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.storeName)
        super(Stores, self).save(*args, **kwargs)

    def __str__(self):
        return self.storeName


class Items(models.Model):
    itemID = models.BigAutoField(unique=True, primary_key=True)
    itemName = models.CharField(max_length=30, unique=True)
    storeID = models.ForeignKey("Stores", on_delete=models.CASCADE)
    sellerID = models.ForeignKey("Sellers", on_delete=models.CASCADE, related_name="itemSellerID")
    sellerName = models.CharField(max_length=30)
    isDigital = models.BooleanField()
    itemDescription = models.CharField(max_length=128)
    itemImage = models.ImageField(upload_to='item_photos/')
    condition = models.CharField(max_length=11, choices=CONDITION_CHOICES)
    listedTime = models.DateTimeField(auto_now_add=True)
    sellTime = models.DateTimeField(null=True, blank=True)
    buyNowPrice = models.DecimalField(decimal_places=2, max_digits=10)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.itemName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.itemName)
        super(Items, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        user = User.objects.get(username=instance.username)
        UserProfile.objects.create(
            user=user,
            description='',
            phoneNo=''
        )
