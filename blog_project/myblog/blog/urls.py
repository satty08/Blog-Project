from django.urls import path
from . import views

urlpatterns = [
    path('',views.PostList.as_view(), name = 'blogpost_list'),
    path('about/', views.About.as_view(), name = 'about'),
    path('post/<int:pk>', views.PostDetail.as_view(), name = 'post_detail'),
    path('post/new/', views.CreatePost.as_view(), name = 'post_new'),
    path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name = 'post_edit'),
    path('post/<int:pk>/remove/', views.PostDelete.as_view(), name = 'post_remove'),
    path('drafts/', views.DraftList.as_view(), name = 'post_draft_list'),
    path('post/<int:pk>/comment/',views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name ='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

]