from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.db.models import Max


from .models import User, Auction_list, Bid, Comment, Category, Image_url, Title


def index(request):
      
    return render(request, "auctions/index.html", {
        "auction_list" : Auction_list.objects.all()
    })


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
        
        # Setting post value int variables
        user_id = request.user.username
        category = request.POST["category"]
        title = request.POST["title"] 
        bid = request.POST["bid"] # int() 적용할지 말지 check
        comment = request.POST["comment"]
        image_url = request.POST["img"]
        time = datetime.now()

        # Saving changes in db by using post value
        create_user_id = User.objects.get(username=f"{user_id}") # create 일렬로 하고 그다음 save 일렬로 하면 제대로 될까?
        create_user_id.save()
        create_category = Category(category=f"{category}")
        create_category.save()
        create_title = Title(title=f"{title}")
        create_title.save()
        create_bid = Bid(user_id=f"{user_id}", bid=f"{bid}")
        create_bid.save()
        create_comment = Comment(comment=f"{comment}")
        create_comment.save()
        create_img_url = Image_url(image_url=f"{image_url}")
        create_img_url.save()
        create_list = Auction_list(user_id=create_user_id, item_category=create_category, item_name=create_title, item_bid=create_bid, item_comment=create_comment, item_img_url=create_img_url, datetime=time)
        create_list.save()

        # Redirecting to index page
        return HttpResponseRedirect(reverse("index")) 


def listpage(request, title): # comment 입력할 수 있게

    # Earning title's id from title which is delivered
    title_object = Title.objects.get(title=title)
    title_id = title_object.id
    tem_bid = Bid.objects.filter(id=title_id)

    # When the method is get
    if request.method == "GET":
        auction_list = Auction_list.objects.filter(item_name=title_id)#title 모델에서 unique 해야할지도?
        biggest_bid = Bid.objects.filter(id=title_id)
        Max_bid = biggest_bid.aggregate(Max('bid'))['bid__max']

        # Listing auction_list into listpage.html page
        return render(request, "auctions/listpage.html", {
            "auction_list" : auction_list,
            "biggest_bid" : Max_bid
        })

    # When the method is post
    else:

        # Saving new bid in db
        username = request.user.username
        update_bid = request.POST["new_bid"]
        tem_bid = Bid(id=title_id, user_id=username, bid=update_bid)
        tem_bid.save()

        # Redirecting to the page post datas come
        return HttpResponseRedirect(reverse("listpage", args=(title,)))


def watchlist(request):
    pass