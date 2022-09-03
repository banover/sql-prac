from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.db.models import Max, Min


from .models import User, Auction_list, Bid, Comment, Category, Image_url, Title,Transaction, Watchlist


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
        create_title = Title(title=f"{title}") # 새로 만든ㄷ게 같은 id라도 덮어쓰지 않고 개별로 만들어지게 하기.
        create_title.save()
        title_id = create_title.id
        create_bid = Bid(user_id=create_user_id, item_name=create_title ,bid=f"{bid}")
        create_bid.save()
        create_comment = Comment(user_id=create_user_id, item_name=create_title, comment=f"{comment}")
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
    #tem_bid = Bid.objects.filter(id=title_id)
    tem_bid = Bid.objects.filter(item_name=title_id)


    # When the method is get
    if request.method == "GET":
        auction_list = Auction_list.objects.filter(item_name=title_object) #Select하는 sql in django syntax에서는 queryset도 되고 queryset.id도 가능 하지만
        #biggest_bid = Bid.objects.filter(id=title_id)                     # Insert할때는 원래 정보를 가진 model에서 get값으로 파라미터 값 넣어줘야함
        total_bid = tem_bid
        Max_bid = total_bid.aggregate(Max('bid'))['bid__max']
        min_bid = total_bid.aggregate(Min('bid'))['bid__min']
        comments = Comment.objects.filter(item_name=title_id)
        loggedin_user = request.user.username
        user_name = User.objects.get(username=loggedin_user)
        seller_name = user_name.id
        tem_username = User.objects.get(username=loggedin_user)
        current_loged_in_username = tem_username.id
        tempory = tem_username.username
        
        transaction = Transaction.objects.filter(item_name=title_id)
        if not len(transaction) == 0:
            bid_winner = Transaction.objects.get(item_name=title_id).buyer            
        else:
            bid_winner = None
        tem_state = auction_list.first()
        state = tem_state.state
     

        # Listing auction_list into listpage.html page
        return render(request, "auctions/listpage.html", {
            "auction_list" : auction_list,
            "biggest_bid" : Max_bid,
            "smallest_bid" : min_bid,
            "next_bid" : float(Max_bid) + 0.01,
            "comments" : comments,
            "loggedin_user" : seller_name,
            "bid_winner" : bid_winner,
            "state" : state,
            "current_loged_in_username" : tempory
        })

    # When the method is post
    else:

        username = request.user.username
        user_id = User.objects.get(username=f"{username}")
        user_id.save()

        # Saving new bid in db
        if 'new_bid' in request.POST:
            
            update_bid = request.POST["new_bid"]            
            item_name_id = Title.objects.get(title=title)                   
            tem_bid = Bid(item_name=item_name_id, user_id=user_id, bid=update_bid)  #item_name_id 대신 id 이건 안됨;
            tem_bid.save()

        # Saving new comment in db
        elif 'new_comment' in request.POST:
            
            update_comment = request.POST["new_comment"]
            item_name_id = Title.objects.get(title=title)
            tem_comment = Comment(user_id=user_id, comment=update_comment, item_name=item_name_id)
            tem_comment.save()

        # Saving new transaction and update state in Auction_list model
        elif 'end_bid' in request.POST:

            # update state "open" to "closed"
            list = Auction_list.objects.filter(item_name=title_id) # update()는 queryset에서 사용가능
            list_state = list.update(state="closed")

            # Setting for saving new transaction
            #title_object = Title.objects.get(title=title)
            #title_id = title_object.id
            #tem_bid = Bid.objects.filter(item_name=title_id)  
            username = request.user.username
            user_id = User.objects.get(username=username)

            name = Title.objects.get(title=title)            
            seller = user_id
            last_bid = tem_bid.aggregate(Max('bid'))['bid__max']
            first_bid = tem_bid.aggregate(Min('bid'))['bid__min']
            starting_bid = tem_bid.get(bid=first_bid)
            selling_price = tem_bid.get(bid=last_bid)
            selling_price_float = float(selling_price.bid)

            buy_user = tem_bid.get(bid=selling_price_float).user_id # queryset으로? 아니면 get값도 가능할까?            
            buyer = User.objects.get(username=buy_user)
            transaction = Transaction(item_name=name, seller=seller, buyer=buyer, starting_bid=starting_bid, selling_price=selling_price)# 다 foreignkey임
            transaction.save()

        elif 'watchlist' in request.POST:
            username = request.user.username
            user_id = User.objects.get(username=f"{username}")
            item_name = request.POST["item_name"]
            list_title = Title.objects.get(title=f"{item_name}").id
            aulist = Auction_list.objects.get(item_name=list_title)# 변수명 중복..조심하자 애초에 설계할때 구조를 잘 짜기..ㅠㅠ
            watchlist = Watchlist(username=user_id, item_name=title_object, list=aulist)
            watchlist.save()



        # Redirecting to the page post datas come
        return HttpResponseRedirect(reverse("listpage", args=(title,)))


def watchlist(request):

    username = request.user.username
    user_id = User.objects.get(username=f"{username}")

    if request.method == "GET":

        watchlist = Watchlist.objects.filter(username=user_id)
        #listname = watchlist.item_name
        #item_name = Title.objects.filter(title=listname)
        #list = Auction_list.objects.filter(item_name=item_name)
        return render(request, "auctions/watchlist.html", {
            "watchlists" : watchlist
        })


    else:
        
        post_item_name = request.POST["delete_item_name"]
        item_name = Title.objects.get(title=post_item_name)
        watchlist = Watchlist.objects.filter(username=user_id, item_name=item_name).delete()

        return HttpResponseRedirect(reverse("watchlist"))