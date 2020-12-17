# define the logic and the order such as adding and removing items from cart

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('TV', 'Television'),
    ('Ph', 'Mobile Phone'),
    ('OW', 'laptop')
)

# Design a user profile


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Design the items field in the database


class Item(models.Model):
    title = models.CharField(max_length=100)
    country_of = CountryField(multiple=False)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    additional_info = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    # Get the product by it's Slug
    def get_absolute_url(self):
        return reverse("main:product", kwargs={
            'slug': self.slug
        })

    # Adding product to the cart in: templates/product.html
    # using function in main/views.py
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })
    # remove product from order list in : templates/order_summary.html
    # using function in main/views.py

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'slug': self.slug
        })

# client add product to the cart


class OrderItem(models.Model):
    # user data
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # number of order that render in cart
    ordered = models.BooleanField(default=False)
    # the product
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # the products' quantity
    quantity = models.IntegerField(default=1)

    # dunder method that returns a products' quantity
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    # to calculate the sum of the price for a specified quantity for a single product
    def get_total_item_price(self):
        return self.quantity * self.item.price

    # to calculate the sum of the discount for a specified quantity for a single product
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    # to calculate the amount of saving from the original product's price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    # to get the prices of the total product if has a discount on it or no
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    # to get the sum of the total money that the client will save it
    def get_final_disc(self):
        if self.item.discount_price:
            return self.get_amount_saved()
        return 0


# handle all the order data
# To calculate all final prices and saving for the order

class Order(models.Model):
    # user data
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # the products
    items = models.ManyToManyField(OrderItem)
    # number of order
    ordered = models.BooleanField(default=False)

    # dunder method that get the user name
    def __str__(self):
        return self.user.username

    # The function will calculate the overall  prices for all products in : templates/order_summary.html
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    # The function will calculate the overall  discount for all products in : templates/order_summary.html
    def get_total_desc(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_disc()
        return total
