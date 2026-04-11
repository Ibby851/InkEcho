from django.urls import path
from . import views
urlpatterns = [
    path('create-blog/', views.blog_create, name='blog_create'),
    path('get-blog/<slug:blog_slug>', views.BlogDetail.as_view(), name="blog_detail"),
    path('blog-list/', views.BlogList.as_view(), name='blog_list'),
    path('search-for-blot/', views.search_blog, name='search_blog')
    
]

htmxpatterns = [
    path('latest-blog/', views.recent_blogs, name='recent_blogs'),
    path('add-or-remove-followers/<str:pen_name>/', views.add_or_remove_followers, name='add_or_remove_followers'),
    path('dashboard/', views.login_redriect, name='login_redirect'),
    path('add-comment/<int:blog_id>/', views.add_blog_comment, name="add_comment"),
    # path('get-comments/<int:blog_id>', views.BlogDetail.as_view(), name='list_blog_comments')
    path('like-or-unlike/<int:blog_id>', views.like_and_unlike, name='like_and_unlike')
]

urlpatterns += htmxpatterns