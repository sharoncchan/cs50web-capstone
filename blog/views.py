from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import User, Category, Post, Comment
from .forms import NewCommentForm
from django.utils.text import slugify
# from django.views.generic import ListView
from django.core.paginator import Paginator




# Create your views here.

def index(request):
    # Get all the posts and order them in reverse chronological order
    posts = Post.objects.all().order_by("-post_date")

     # Display 6 posts per page
    paginator = Paginator(posts, per_page=6)
    categories = Category.objects.all()

    # Create a page number variable that request for the current page number
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html",{
        "posts":posts,
        "page_obj":page_obj,
        "categories" : categories
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
            error = True
            return render(request, "blog/login.html", {
                "message": "The username or password you entered is incorrect. Please try again keying in the correct username and password",
                "error" : error
            })
    else:
        return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # Get the details from the form filled in
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        user_avatar = request.POST["user_avatar"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            error = True
            return render(request, "blog/register.html", {
                "message": "Passwords must match.",
                "error" : error
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, user_avatar = user_avatar)
            user.save()
        except IntegrityError:
            error = True
            return render(request, "blog/register.html", {
                "message": "Username already taken. Please try another username",
                "error" : error
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blog/register.html")


@login_required
def create_post(request):
    # If user submit the form
    if request.method == "POST":
        # Get all the values filled in the form and save into the Post database
        title = request.POST["title"]
        name_category = request.POST["category"]
        category = Category.objects.get(name=name_category)
        reading_duration = request.POST["reading_duration"]
        image = request.POST["image"]
        content = request.POST["content"]

        poster_avatar = request.user.user_avatar
        Post.objects.create(poster=request.user, category = category, title = title, slug = slugify(title), body = content, reading_duration = reading_duration,image = image, poster_avatar = poster_avatar)
        
        return HttpResponseRedirect(reverse("index"))

    # If user reach route via GET
    else:
        categories = Category.objects.all()
        return render(request, "blog/create.html",{
            "categories" : categories
        })

def post(request, post_slug):
    # Get the post being requested for
    individual_post = Post.objects.get(slug = post_slug)

    # Get the comments of the post
    post_comments = Comment.objects.filter(post = individual_post)

    # If user try to add a comment
    if request.method == "POST":
        # Check if user is logged in 
        if request.user.is_authenticated:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.username = request.user
                user_comment.post = individual_post
                user_comment.comment_avatar = request.user.user_avatar
                user_comment.save()
                return HttpResponseRedirect(reverse("post", args=(post_slug,)))
        else:
            comment_form = NewCommentForm
            return render(request, "blog/post.html",{
                "post" : individual_post,
                "comments" : post_comments,
                "comment_form" : comment_form,
            })
    # If user reach route via GET
    else:
        comment_form = NewCommentForm
        return render(request, "blog/post.html",{
        "post" : individual_post,
        "comments" : post_comments,
        "comment_form" : comment_form,
    })

   
    

def category(request, category_name):
     # Get the category being requested for
     category = Category.objects.get(name = category_name)

     # Get all the posts in the category
     posts = Post.objects.filter(category = category)

     # Display 6 posts per page
     paginator = Paginator(posts, per_page = 6)
    
     # Create a page number variable that request for the current page number
     page_number = request.GET.get("page")
     page_obj = paginator.get_page(page_number)

     # Exclude the current category
     other_categories = Category.objects.exclude(name = category_name)

     return render(request, "blog/category.html",{
        "posts" : posts,
        "page_obj":page_obj,
        "category": category,
        "other_categories" : other_categories
    })

@login_required
def bookmark(request, post_id):
    # Retrieve the details from the POST request

    # Submitting a bookmark/remove bookmark must be via POST, check if its a POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"},
            status = 400
        )

    # Get the id of the post
    data = json.loads(request.body)
    post_id = int(data.get("post_id"))

    # Check if post has been bookmarked by the user
    post = Post.objects.get(id = post_id)
    
    if request.user not in post.bookmarks.all():
            # Add the post into the user bookmarks
            post.bookmarks.add(request.user)
            post.save()
            return JsonResponse({
                "bookmark":"True",
                "message" : "This post have been added into user's bookmarks"
            }, status =200)

    else:
        # Remove the post from the user bookmarks
        post.bookmarks.remove(request.user)
        post.save()
        return JsonResponse({
            "bookmark":"False",
            "message" : "This post have been removed from user's bookmarks"
        }, status=200)


@login_required
def bookmarks(request):
    # Get all the posts where the bookmarks contains the current user
    posts =  Post.objects.filter(bookmarks = request.user)

     # Display 6 posts per page
    paginator = Paginator(posts, per_page = 6)
    
    # Create a page number variable that request for the current page number
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/bookmarks.html",{
        "posts" : posts,
        "page_obj":page_obj
    })


def profile(request, profile_name):
    # Get the user 
    profile_user = User.objects.get(username = profile_name)

    # Get all the posts the user has posted
    posts =  Post.objects.filter(poster = profile_user)

    # Display 6 posts per page
    paginator = Paginator(posts, per_page = 6)
    
    # Create a page number variable that request for the current page number
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/profile.html",{
        "posts" : posts,
        "page_obj":page_obj,
        "profile_user" : profile_user
    })


@login_required
def like(request, post_id):
    # Retrieve the details from the POST request

    # Submitting a like/unlike must be via POST, check if its a POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"},
            status = 400
        )

    # Get the id of the post
    data = json.loads(request.body)
    post_id = int(data.get("post_id"))

    # Check if post has been liked by the user
    post = Post.objects.get(id = post_id)
    
    if request.user not in post.likes.all():
        # Add the post into the user bookmarks
        post.likes.add(request.user)
        post.save()
        num_likes = post.likes.count()
        return JsonResponse({
            "like":"True",
            "message" : "The user has liked this post",
            "num_likes" : num_likes
        
        }, status =200)

    else:
        # Remove the post from the user bookmarks
        post.likes.remove(request.user)
        post.save()
        num_likes= post.likes.count()
        return JsonResponse({
            "like":"False",
            "message" : "The user has unliked this post",
            "num_likes" : num_likes
        }, status=200)



@login_required
def edit(request, post_id):
     # Retrieve the details from the POST request

    # Submitting a edit must be via POST, check if its a POST request
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"},
            status = 400
        )

    # Get the id and edited content of the post
    data = json.loads(request.body)
    post_id = int(data.get("post_id"))
    edited_content = data.get("edited_content")

    # Update and save the edited post
    post = Post.objects.get(id = post_id)
    post.body = edited_content
    post.save()

    return JsonResponse({
            "message": "Post has been edited and saved"},
            status = 200
        )









    





