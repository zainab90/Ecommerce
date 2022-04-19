from django.contrib.auth import authenticate, login, logout
from django.core.mail.backends import console
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import AuctionForm, CategoryForm, BidForm, AddComment
from .models import User, Auction, Catogery, Comment


def index(request):
    active_list = Auction.objects.all().filter(active=True)
    return render(request, 'auctions/index.html', {'active_list': active_list})





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






def add_category(request):
    creatCategForm=CategoryForm()
    if request.method =='POST':
        creatCategForm=CategoryForm(request.POST)
        if creatCategForm.is_valid():
            creatCategForm.save()
            return redirect('category-list')
    return render (request,'auctions/addCategory.html',{'creatCategForm':creatCategForm})



def category_list(request):
    category_list = Catogery.objects.all()
    return render(request, 'auctions/catogeryList.html', {'category_list': category_list})


def show_category(request, id):
    active_list = Auction.objects.all().filter(catogery_id=id)
    return render(request, 'auctions/index.html' , {'active_list':active_list})


def show_listing(request,id):
    active_list = Auction.objects.all().filter(id=id)
    bidForm=BidForm()
    commentForm=AddComment()
    comment_list=Comment.objects.all().filter(auctions_id=id)
    print(active_list)
    return render(request, 'auctions/showListingItem.html' , {'active_list':active_list, 'id': id, 'bidForm': bidForm,'commentForm':commentForm, 'comment_list':comment_list})


def add_comment(request, id):
    creatComment= AddComment()
    active_list = Auction.objects.all().filter(id=id)
    bidForm = BidForm()
    comment_list = Comment.objects.all().filter(auctions_id=id)
    if request.method == 'POST':
        creatComment = AddComment(request.POST)
        if creatComment.is_valid():
            creatComment.instance.user = request.user
            creatComment.save()
            return render(request, 'auctions/showListingItem.html',
                           {'active_list': active_list, 'id': id,
                            'bidForm':bidForm,
                            'commentForm': creatComment,
                            'comment_list':comment_list})
        else:
            pass


def add_bid(request, id):
    creatBid = BidForm()
    creatComment = AddComment()
    active_list = Auction.objects.all().filter(id=id)
    comment_list = Comment.objects.all().filter(auctions_id=id)
    if request.method=='POST':
        creatBid = BidForm(request.POST)
        if creatBid.is_valid():
            creatBid.instance.user=request.user
            creatBid.save()
            return render(request, 'auctions/showListingItem.html' ,
                          {'active_list':active_list,
                           'id': id,
                           'bidForm': creatBid,
                           'commentForm':creatComment,
                           'comment_list':comment_list
                           })
        else:
            pass







