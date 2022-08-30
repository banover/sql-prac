from django.contrib.auth.models import AbstractUser
from django.db import models

class Image_url(models.Model):
    image_url = models.CharField(max_length=64, default=None)

    def __str__(self):
        return f"img_url : {self.image_url}"


class Category(models.Model):
    category = models.CharField(max_length=64, default=None)

    def __str__(self):
        return f" category : {self.category}"


class Comment(models.Model):
    comment = models.CharField(max_length=500, default=None)

    def __str__(self):
        return f"comment : {self.comment}"


class Bid(models.Model):
    user_id = models.CharField(max_length=30, default=None)
    #item_name = models.ForeignKey(Auction_list, ) #title 따로 model 만든 다음에 foreingkey로 설정하자 
    bid = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return f"price : {self.bid}$ buyer : {self.user_id}"


class Auction_list(models.Model): #title도 따로빼자
    user_id = models.CharField(max_length=30, default=None)
    item_category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="item_category")
    item_name = models.CharField(max_length=64)
    item_bid =  models.ForeignKey(Bid, default=0.00, on_delete=models.PROTECT, related_name="item_bid")
    item_comment = models.ForeignKey(Comment, default=None, on_delete=models.PROTECT, related_name="item_comment")
    item_img_url = models.ForeignKey(Image_url, default=None, on_delete=models.PROTECT, related_name="item_img_url")
    datetime = models.DateTimeField()

    def __str__(self):
        return f"id : {self.id} seller : {self.user_id} | {self.item_category}, item = {self.item_name}, {self.item_bid}, {self.item_comment}, {self.item_img_url}, time = {self.datetime}"


class User(AbstractUser):
    pass


