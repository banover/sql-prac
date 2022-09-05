from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name ="create"),
    path("listpage/<str:title>", views.listpage, name="listpage"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("category/", views.category, name="category"),
    path("category_listpage/<str:category>", views.category_listpage, name="category_listpage")
]
