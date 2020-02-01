
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="shopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("track/", views.tracker, name="Tracker"),
    path("search/", views.searcher, name="Search"),
    path("products/<int:myId>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="CheckOut"),

]