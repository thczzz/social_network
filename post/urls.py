from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    path('add/', views.CreatePostView.as_view(), name='add-post'),
    path('view/<int:user_id>/', views.UserPostsView.as_view(), name='view-posts-by-user'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='like-post'),
    path('comment/<int:post_id>/', views.PostCommentView.as_view(), name='comment-post'),
    path('wall/', views.PostsWallView.as_view(), name='wall'),
]
