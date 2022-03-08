from django.db import IntegrityError
from django.db.models import Count
from rest_framework.response import Response
from post import serializers, models
from rest_framework import permissions, generics, status
from rest_framework.pagination import LimitOffsetPagination


class CreatePostView(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        data = {
            'creator': request.user.id,
            'post_text': request.data.get('post_text'),
        }

        post_image = request.data.get('post_image')
        if post_image != '':
            data["post_image"] = post_image

        serializer = serializers.PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostsView(generics.RetrieveAPIView):
    queryset = models.Post.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = serializers.PostSerializer

    def retrieve(self, request, *args, **kwargs):
        creator_id = kwargs.get("user_id", None)
        if creator_id is not None:
            queryset = models.Post.objects.filter(creator_id=creator_id).order_by('-created_at')
            serializer = serializers.PostSerializer(queryset, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostLikeView(generics.CreateAPIView):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id", None)
        if post_id is not None:
            try:
                like = models.PostLike.objects.create(
                    user=request.user,
                    post_id=post_id
                )
            except IntegrityError:
                # unlike
                like = models.PostLike.objects.get(user=request.user, post_id=post_id)
                like.delete()
                return Response('Unliked', status=status.HTTP_200_OK)
            return Response('Liked', status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PostCommentView(generics.CreateAPIView):
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id", None)
        if post_id is not None:
            comment = request.data.get("comment")
            models.PostComment.objects.create(
                user_id=request.user.id,
                post_id=post_id,
                comment=comment
            )
            return Response('Comment posted', status=status.HTTP_201_CREATED)


class PostsWallView(generics.RetrieveAPIView, LimitOffsetPagination):
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):

        queryset = models.Post.objects.prefetch_related('likes', 'comments').filter(
            creator__in=request.user.friends.all()).annotate(likes_count=Count('likes')).annotate(
            comments_count=Count('comments')).order_by('-created_at', '-comments_count', '-likes_count')

        results = self.paginate_queryset(queryset)
        serializer = serializers.PostSerializer(results, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
