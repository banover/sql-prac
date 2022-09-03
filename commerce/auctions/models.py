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
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="comment_user")
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="comment_item_name")
    comment = models.CharField(max_length=500, default=None) # user_id 정보 등록하기


    def __str__(self):
        return f"comment : {self.comment}"


class Bid(models.Model): # 제일 큰 bid값이 page에 뜨게끔 설정
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="bid_user")
    #user_id = models.CharField(max_length=30, default=None)
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="Bid_item_name") 
    bid = models.FloatField()
    

    def __str__(self):
        return f"{self.bid}$"


class Transaction(models.Model):
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="tran_item_name")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="tran_seller_user")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="tran_buyer_user")
    starting_bid = models.ForeignKey(Bid, default=0.00, on_delete=models.PROTECT, related_name="tran_st_bid")
    selling_price = models.ForeignKey(Bid, default=0.00, on_delete=models.PROTECT, related_name="tran_selling_price")





class Auction_list(models.Model): # auction_list랑 bid를 연결하는 새로운 모델을 만들어서 활용한다면? or Bid에 title을 추가? 두개다 해보자 ㅋ
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="user")
    item_category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, related_name="item_category")
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="item_name")    
    item_bid =  models.ForeignKey(Bid, default=0.00, on_delete=models.PROTECT, related_name="item_bid")
    item_comment = models.ForeignKey(Comment, default=None, on_delete=models.PROTECT, related_name="item_comment")
    item_img_url = models.ForeignKey(Image_url, default=None, on_delete=models.PROTECT, related_name="item_img_url")
    datetime = models.DateTimeField()
    state = models.CharField(max_length=6, default="open")
    # state 하나 만들어서 open/closed 기입해야할듯

    def __str__(self):
        return f"id : {self.id} seller : {self.user_id} | {self.item_category}, {self.item_name}, {self.item_bid}, {self.item_comment}, {self.item_img_url}, time = {self.datetime}, state = {self.state}"


class Watchlist(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, related_name="watchlist_user")
    item_name = models.ForeignKey(Title, default=None, on_delete=models.CASCADE, related_name="watchlist_item_name")
    list = models.ForeignKey(Auction_list, default=None, on_delete=models.CASCADE, related_name="watchlist_list")

    def __str__(self):
        return f"{self.username} {self.item_name}"
        

class User(AbstractUser):
    pass


