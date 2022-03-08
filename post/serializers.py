from rest_framework import serializers
from post import models
from user.serializers import UserSerializer


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostLike
        exclude = ('id',)


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = models.PostComment
        exclude = ('id',)


class LikesListingField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value.username


class PostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(allow_empty_file=True, required=False)
    created_at = serializers.DateTimeField(source='format_timesince', required=False)
    comments = PostCommentSerializer(source='post_comments', many=True, read_only=True)
    likes = LikesListingField(many=True, read_only=True)
    # post_image = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = models.Post
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'likes': {'read_only': True},
            'comments': {'read_only': True},
            'created_at': {'read_only': True},

        }

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation["creator"] = instance.creator.username
        return representation

    # def get_post_image(self, obj):
    #     return self.context["request"].build_absolute_uri(obj.post_image.url)
