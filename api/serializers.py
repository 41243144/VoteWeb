from rest_framework import serializers
from api.models.Profile import Profile
from api.models.Post import Post, Comment
from api.models.Category import Category
from api.models.Tag import Tag

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['studient_id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'create_user', 'created_at', 'updated_at']
        read_only_fields = ['create_user', 'created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    '''
    tags: 這是一個 write_only 的欄位，用來接收一個 list of string
    category: 這是一個 read_only 的欄位，用來顯示 category 的名稱
    studient_id: 這是一個 read_only 的欄位，用來顯示 profile 的 studient_id

    create: 這個方法會在建立一個新的 post 時被呼叫
    update: 這個方法會在更新一個 post 時被呼叫

    '''
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    studient_id = serializers.CharField(write_only=False, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'link', 'category', 'tags', 'studient_id', 'created_at', 'updated_at', 'views', 'slug']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        studient_id = validated_data.pop('studient_id', None)
        post = Post.objects.create(studient_id=studient_id, **validated_data)

        for tag_string in tags_data:
            tag_names = tag_string.split(',')
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip(), defaults={'create_user': self.context['request'].user})
                post.tags.add(tag)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        studient_id = validated_data.pop('studient_id', None)
        instance.studient_id = studient_id
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.link = validated_data.get('link', instance.link)
        instance.category = validated_data.get('category', instance.category)

        if tags_data:
            instance.tags.clear()
            for tag_string in tags_data:
                tag_names = tag_string.split(',')
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.strip(), defaults={'create_user': self.context['request'].user})
                    instance.tags.add(tag)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    '''
    post: 這是一個 read_only 的欄位，用來顯示 post 的 title
    profile: 這是一個 read_only 的欄位，用來顯示 profile 的 studient_id
    content: 這是一個 write_only 的欄位，用來接收 comment 的內容
    created_at: 這是一個 read_only 的欄位，用來顯示 comment 的建立時間
    updated_at: 這是一個 read_only 的欄位，用來顯示 comment 的更新時間
    
    '''
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        post = validated_data.pop('post')
        profile = validated_data.pop('profile')
        comment = Comment.objects.create(post=post, profile=profile, **validated_data)
        return comment