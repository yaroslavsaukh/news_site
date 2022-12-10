from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    #path('', index, name='home'),
    #path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsCategoryList.as_view(), name='category'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news', CreateNews.as_view(), name='add_news'),
    path('news/add-category', CreateCat.as_view(), name='add_category'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('feedback/', send_email, name='feedback')
]