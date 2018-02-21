from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'test_dashboard$', views.test_wish_list),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^add_item$', views.added_item),
    url(r'logout$', views.logout),
    url(r'dashboard$', views.wish_list),
    url(r'create$', views.create),
    url(r'^add_wish/(?P<item_id>\d+)$', views.add_wish),
    url(r'^unwish/(?P<item_id>\d+)$', views.unwish),
    url(r'wish_item/(?P<item_id>\d+)$', views.items),
    url(r'destroy/(?P<item_id>\d+)$', views.destroy),
    url(r'update/(?P<item_id>\d+)$', views.update),    
    url(r'other_items$', views.other_items),
    url(r'about$', views.about),
    url(r'contact$', views.contact),
    url(r'edit/(?P<item_id>\d+)$', views.edit),
    url(r'delete/(?P<item_id>\d+)$', views.delete),
    url(r'wishlists$', views.wishlists),
] 