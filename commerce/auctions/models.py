from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Title(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Image_url(models.Model):
    image_url = models.CharField(max_length=500, default=None)

    def __str__(self):
        return f"{self.image_url}"


class Category(models.Model):
    category = models.CharField(max_length=64, default=None)

    def __str__(self):
        return f"{self.category}"


class Comment(models.Model): # comment가 다른 id로 부터도 저장이되고 출력이 되게, title,user_id도 같이 등록해야할듯
    comment = models.CharField(max_length=500, default=None) # user_id 정보 등록하기

    def __str__(self):
        return f"comment : {self.comment}"


class Bid(models.Model): # 제일 큰 bid값이 page에 뜨게끔 설정
    user_id = models.CharField(max_length=30, default=None)
    #item_name = models.ForeignKey(Auction_list, ) 
    bid = models.FloatField()
    

    def __str__(self):
        return f"{self.bid}$"


class Auction_list(models.Model): # auction_list랑 bid를 연결하는 새로운 모델을 만들어서 활용한다면?
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="user")
    item_category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="item_category")
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="item_name")    
    item_bid =  models.ForeignKey(Bid, default=0.00, on_delete=models.PROTECT, related_name="item_bid")
    item_comment = models.ForeignKey(Comment, default=None, on_delete=models.PROTECT, related_name="item_comment")
    item_img_url = models.ForeignKey(Image_url, default=None, on_delete=models.PROTECT, related_name="item_img_url")
    datetime = models.DateTimeField()

    def __str__(self):
        return f"id : {self.id} seller : {self.user_id} | {self.item_category}, {self.item_name}, {self.item_bid}, {self.item_comment}, {self.item_img_url}, time = {self.datetime}"


class User(AbstractUser):
    pass


