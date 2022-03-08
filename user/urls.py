from django.urls import path
from user import views

urlpatterns = [
    path('friends/<int:user_id>/', views.FriendsView.as_view(), name='get-friends'),
    path('send-friend-request/<int:to_user>/', views.SendFriendRequestView.as_view(), name='send-friend-req'),
    path('friend-requests/', views.ViewFriendRequestsView.as_view(), name='get-friend-requests'),
    path('friend-requests/<int:friend_req_id>/', views.AcceptFriendRequestView.as_view(), name='accept-friend-req'),
]
