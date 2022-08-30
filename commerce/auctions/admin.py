from django.contrib import admin
from .models import Bid, Auction_list, Comment, User, Category, Image_url

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_list)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Image_url)