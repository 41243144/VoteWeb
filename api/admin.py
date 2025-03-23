from django.contrib import admin
from api.models.Profile import Profile
from api.models.Category import Category
from api.models.Tag import Tag
from api.models.Post import Post, Comment, PostLike
from django.contrib.auth.models import User
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'studient_id', 'name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('user__username', 'studient_id', 'name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_user', 'created_at', 'updated_at')
    search_fields = ('name', 'create_user__username')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ 限制 create_user 只能選擇管理員 """
        if db_field.name == "create_user":
            kwargs["queryset"] = User.objects.filter(is_superuser=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username', 'category__name')
    list_filter = ('category', 'tags', 'created_at')
    # prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('views', 'created_at', 'updated_at')

    


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'profile', 'content', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')

class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)

