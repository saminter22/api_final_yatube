from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(queryset=Follow.objects.all(),
                                                fields=('user', 'following'),
                                                message='Подписка невозможна')
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        return value

    # def validate(self, data):
    #     if self.context['request'].user == data['following']:
    #         raise serializers.ValidationError('Нельзя подписаться на себя!')
    #     return data
