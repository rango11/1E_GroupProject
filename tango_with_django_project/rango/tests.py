from django.test import TestCase
# Create your tests here.
class SellerMethodTests(TestCase):
    def test_slug_line_creation(self):
        seller = Seller(userID = x, sellerName = "Bob's Premier Collection", rating = 2)
        seller.save()

        self.assertEqual(category.slug, "bob's-premier-collection")

    def test_rating_is_non_negative(self):
        seller = Seller(userID = x, sellerName = "Bob's Premier Collection", rating = -1)
        seller.save()
        self.assertEqual(seller.views >= 0, True, f"Seller rating should be non negative. Instead rating of {seller.rating} was recieved")
    
    