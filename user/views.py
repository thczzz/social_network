from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework import permissions, generics, status


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer


class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        to_user_pk = kwargs.get("to_user", None)
        if to_user_pk is not None:
            to_user = get_object_or_404(models.User, id=to_user_pk)
            from_user = request.user

            if from_user.id == to_user.id:
                return Response("You can't send a friend request to yourself :(", status=status.HTTP_400_BAD_REQUEST)

            if from_user in to_user.friends.all():
                return Response('Already friends', status=status.HTTP_400_BAD_REQUEST)

            friend_request, created = models.FriendRequest.objects.get_or_create(
                from_user=from_user, to_user=to_user
            )
            if created:
                return Response('Friend request sent.', status=status.HTTP_201_CREATED)
            else:
                return Response('Friend request was already sent.', status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ViewFriendRequestsView(generics.RetrieveAPIView):
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = models.FriendRequest.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = models.FriendRequest.objects.filter(to_user=request.user)
        serializer = serializers.FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class AcceptFriendRequestView(generics.CreateAPIView):
    serializer_class = serializers.AcceptFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        friend_request_id = kwargs["friend_req_id"]
        friend_req = get_object_or_404(models.FriendRequest, id=friend_request_id)
        if friend_req.to_user == request.user:
            friend_req.to_user.friends.add(friend_req.from_user)
            friend_req.from_user.friends.add(friend_req.to_user)

            friend_req.delete()
            return Response(f"You and {friend_req.from_user} are now friends.", status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendsView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id", None)
        if user_id is not None:
            user = get_object_or_404(models.User, id=user_id)
            queryset = user.friends.all()
            serializer = serializers.UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
