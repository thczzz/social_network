from rest_framework import serializers
from user import models


# class FriendsListingField(serializers.RelatedField):
#     def to_internal_value(self, data):
#         pass
#
#     def to_representation(self, value):
#         return value.username


class UserSerializer(serializers.ModelSerializer):
    # friends = FriendsListingField(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ('username',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = [
            'username',
            'password',
            'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = models.User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FriendRequest
        fields = ['id', 'from_user', 'to_user']
        extra_kwargs = {
            'from_user': {'read_only': True},
            'id': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super(FriendRequestSerializer, self).to_representation(instance)
        representation["from_user"] = instance.from_user.username
        representation["to_user"] = instance.to_user.username
        return representation


class AcceptFriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FriendRequest
        fields = ['id',]
        extra_kwargs = {
            'id': {'read_only': True}
        }
