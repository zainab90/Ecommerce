from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail.backends import console
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import AuctionForm, CategoryForm, BidForm, AddComment
from .models import User, Auction, Catogery, Comment, WatchList, Bid


def index(request):
    active_list = Auction.objects.all().filter(active=True)
    return render(request, 'auctions/index.html', {'active_list': active_list})

@login_required
def show_watching_list(request, un):
    myList=[]
    watc_obj=WatchList.objects.all().filter(user=request.user)
    for item in watc_obj:
        if item.auctions.active:
            myList.append(item.auctions)



    return render(request, 'auctions/index.html', {'active_list': myList})


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

@login_required
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

@login_required
def create_listing(request):
    m=""
    createForm=AuctionForm(initial={
        'user' : request.user
    })
    if request.method=='POST':
        createForm=AuctionForm(request.POST)
        if createForm.is_valid():
            createForm.instance.user = request.user
            createForm.instance.active = True
            print(request.user)
            createForm.save()
            return redirect('index')
        else:
            m="error in validity"

    return render(request,'auctions/createListing.html',{'creatForm':createForm,'m':m})

@login_required
def add_category(request):
    creatCategForm=CategoryForm()
    if request.method =='POST':
        creatCategForm=CategoryForm(request.POST)
        if creatCategForm.is_valid():
            creatCategForm.save()
            return redirect('category-list')
    return render (request,'auctions/addCategory.html',{'creatCategForm':creatCategForm})


@login_required
def category_list(request):
    category_list = Catogery.objects.all()
    return render(request, 'auctions/catogeryList.html', {'category_list': category_list})

@login_required
def show_category(request, id):
    active_list = Auction.objects.all().filter(catogery_id=id, active=True)
    return render(request, 'auctions/index.html' , {'active_list':active_list})
@login_required
def close_listing(request,id):
    active_list = Auction.objects.all().get(id=id)
    active_list.active=False
    active_list.save()
    its_auction=Bid.objects.all().filter(auctions=active_list)
    its_bid=[item.bid for item in its_auction]
    try:
        higher_bid = max(its_bid)

    except ValueError:
         higher_bid = 0

    try:
        us = Bid.objects.all().get(bid=higher_bid, auctions=active_list).user.username
    except Exception:
        us=''
    print(us)
    message = ''
    mess_comment = ''
    remove_stats = 'visible'
    close_status = 'enabled'
    bid_status = 'enabled'
    add_status = 'enabled'
    bidForm = BidForm()
    commentForm = AddComment()
    comment_list = Comment.objects.all().filter(auctions_id=id)
    ac_user = Auction.objects.all().get(id=id).user.username
    watch = WatchList.objects.filter(auctions_id=id, user=request.user)
    if watch:
        btn_value = 'Remove From Watch List'
        fill_stat = 'fill'
    else:
        # save in watchlist
        btn_value = 'ADD to Watch List'
        fill_stat = 'none'

    if ac_user == request.user.username:
        close_btn = 'block'

    else:
        close_btn = 'none'
    return render(request, 'auctions/showListingItem.html',
                  {'btn_value': btn_value,
                   'close_btn': close_btn,
                   'active_list': Auction.objects.all().filter(id=id),
                   'id': id,
                   'message': message,
                   'mess_comment': mess_comment,
                   'bidForm': bidForm,
                   'commentForm': commentForm,
                   'comment_list': comment_list,
                   "remove_stats": remove_stats,
                   "close_status": close_status,
                   "bid_status": bid_status,
                   "add_status": add_status,
                   "fill_stat": fill_stat,
                   'txt_color': "text-primary",
                   'winner': 'flex',
                   'winner_name':us,
                   'item_body': 'none'
                   })

@login_required
def show_listing(request,id):
    message=''
    txt_color='text-primary'
    active_list = Auction.objects.all().filter(id=id)
    bidForm=BidForm()
    commentForm=AddComment()
    comment_list=Comment.objects.all().filter(auctions_id=id)
    if request.method == 'POST':
        creatBid = BidForm(request.POST)
        if creatBid.is_valid():
            creatBid.instance.user = request.user
            user_auctions = Auction.objects.all().get(id=id)
            creatBid.instance.auctions = user_auctions
            u_bid = creatBid.cleaned_data['bid']
            start_bd = Auction.objects.all().get(id=id).start_bid

            flg = check_on_otherBids(u_bid, user_auctions)
            if u_bid > start_bd and flg:
                active_listx = Auction.objects.all().get(id=id)
                active_listx.start_bid = u_bid
                active_listx.save()
                creatBid.save()
                message = 'the current bid is your bid'
                txt_color='text-primary'
            else:
                message = 'start bid or other previous bids is greatar than your bid'
                txt_color='text-danger'

        else:
            pass
    if request.user.is_anonymous:
        message = 'you can not place bide to this item, Log in first!'
        mess_comment = 'you can not write comment on this item, Log in first!'
        remove_stats = 'hidden'
        close_status = 'disabled'
        bid_status = 'disabled'
        add_status = 'disabled'
        btn_value = 'Add/ Remove watchlist'
        close_btn = 'none'
        fill_stat = 'none'
        txt_color='text-danger'
    else:
        message = message
        mess_comment = ''
        remove_stats = 'visible'
        close_status = 'enabled'
        bid_status = 'enabled'
        add_status = 'enabled'
        txt_color=txt_color
        ac_user = Auction.objects.all().get(id=id).user.username
        watch = WatchList.objects.filter(auctions_id=id, user=request.user)
        if watch:
            btn_value = 'Remove From Watch List'
            fill_stat = 'fill'
        else:
            # save in watchlist
            btn_value = 'ADD to Watch List'
            fill_stat = 'none'

        if ac_user == request.user.username:
            close_btn = 'block'

        else:
            close_btn = 'none'



    return render(request, 'auctions/showListingItem.html' ,
                  {'btn_value':btn_value,
                   'close_btn':close_btn,
                    'active_list':active_list,
                   'id': id,
                   'message':message,
                   'mess_comment':mess_comment,
                   'bidForm': bidForm,
                   'commentForm':commentForm,
                   'comment_list':comment_list,
                   "remove_stats" : remove_stats,
                   "close_status" : close_status,
                   "bid_status" :bid_status,
                   "add_status" : add_status,
                   "fill_stat" : fill_stat,
                   'txt_color': txt_color,
                   'winner':'none',
                   'winner_name': '',
                   'item_body':'flex'
                   })

@login_required
def add_comment(request, id):
    if request.method == 'POST':
        creatComment = AddComment(request.POST)
        if creatComment.is_valid():
            creatComment.instance.user = request.user
            creatComment.instance.auctions= Auction.objects.all().get(id=id)
            creatComment.save()
            return HttpResponseRedirect(reverse('show-listing', args=(id,)))

        else:
            pass


def check_on_otherBids(u_bid, a):
    print('user_bid',u_bid)
    res=[]
    tot=[]
    res=Bid.objects.all().filter(auctions=a)
    tot=[item.bid for item in res]
    try:
        max_bid=max(tot)

    except ValueError:
        max_bid = 0

    if u_bid> max_bid:
        print('true')
        return True
    else:
        print('false')
        return False








@login_required
def add_watchList(request, id):

    watch = WatchList.objects.filter(auctions_id=id, user=request.user)
    print('watch', watch)
    if watch:
        watch.delete()
        btn_value = 'ADD to Watch List'
        fill_stat='none'
    else:
        # save in watchlist
        btn_value = 'Remove From Watch List'
        fill_stat='fill'
        WatchList.objects.create(
            user=request.user,
            auctions_id=id
        )
    return HttpResponseRedirect(reverse('show-listing', args=(id,)))








