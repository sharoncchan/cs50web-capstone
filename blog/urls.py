from django.urls import path
from . import views 



urlpatterns= [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("post/<slug:post_slug>", views.post, name="post"),
    path("category/<str:category_name>", views.category, name="category"),
    path("bookmarks", views.bookmarks, name="bookmarks"),
    path("profile/<str:profile_name>", views.profile, name="profile"),
   

    # API Routes
    path("bookmark/<str:post_id>", views.bookmark, name="bookmark"),
    path("like/<str:post_id>", views.like, name="like"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    
]