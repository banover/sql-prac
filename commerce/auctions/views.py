from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime


from .models import User, Auction_list, Bid, Comment, Category, Image_url


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")

    else:
        category = request.POST["category"]
        title = request.POST["title"] # 따로 model 만들 예정 만든후 밑에 insert작문하기
        bid = request.POST["bid"] # int() 적용할지 말지 check
        comment = request.POST["comment"]
        image_url = request.POST["img"]
        time = datetime.now()

        create_category = Category(category=f"{category}")
        create_category.save()
        create_bid = Bid()
        create_bid.save()
        create_comment = Comment(comment=f"{comment}")
        create_comment.save()
        create_img_url = Image_url(image_url=f"{image_url}")
        create_img_url.save()
        create_list = Auction_list(user_id="", item_category=create_category, item_name="", item_bid=create_bid, item_comment=create_comment, item_img_url=create_img_url, datetime=time)
        create_list.save()

from .models import User, Auction_list, Bid, Comment, Category, Image_url



