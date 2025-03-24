import pandas as pd
from django.http import HttpResponse
from django.db.models import Count, Max, Subquery, OuterRef, Sum
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from api.models.Profile import Profile
from api.models.Post import Post, PostLike, Comment
from api.models.Category import Category
from api.models.Tag import Tag
from api.serializers import ProfileSerializer, PostSerializer, CategorySerializer, TagSerializer, CommentSerializer



class ProfileView(viewsets.ModelViewSet):
    '''
    1. queryset: 資料庫查詢的資料集
    2. serializer_class: 使用的序列化器為ProfileSerializer
    3. permission_classes: 使用的權限類別為登入者才能存取

    function:
        1. create:
            method: POST
            url: api/profile/create/
            func: 創建使用者的個人資料

        2. update:
            method: PUT
            url: api/profile/update/
            func: 更新使用者的個人資料

        3. list:
            method: GET
            url: api/profile/
            func: 取得使用者的個人資料

    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        '''
            取得使用者的個人資料
        '''
        return Profile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        '''
            創建使用者的個人資料
        '''
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        '''
            更新使用者的個人資料
        '''
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        '''
            儲存使用者的個人資料
        '''
        serializer.save()

    def list(self, request, *args, **kwargs):
        '''
            覆寫 list 方法以移除分頁資訊
        '''
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostView(viewsets.ModelViewSet):
    '''
    1. queryset: 資料庫查詢的資料集
    2. serializer_class: 使用的序列化器為PostSerializer
    3. permission_classes: 使用的權限類別為登入者才能存取

    function:
        1. counter_data:
            method: GET
            url: api/post/counter-data/
            func: 取得計數器數據

        2. get_all_posts:
            method: GET
            url: api/post/all_posts/
            func: 取得所有文章

        3. get_post_by_slug:
            method: GET
            url: api/post/article/<slug>/
            func: 取得文章的詳細資訊

        4. get_latest_posts:
            method: GET
            url: api/post/latest/
            func: 取得最新文章

        5. get_posts_by_tag:
            method: GET
            url: api/post/by-tag/<tag_name>/
            func: 取得標籤名稱為<tag_name>的所有文章

        6. get_post_details:
            method: GET
            url: api/post/details/
            func: 取得文章的詳細資訊

        7. get_post_detail:
            method: GET
            url: api/post/<pk>/detail/
            func: 取得文章的詳細資訊

        8. get_leaderboard:
            method: GET
            url: api/post/leaderboard/
            func: 取得文章的排行榜

        9. export_leaderboard:
            method: GET
            url: api/post/export-leaderboard/
            func: 匯出文章排行榜為 CSV

        10. like_post:
            method: POST
            url: api/post/<pk>/like_post/
            func: 按讚文章

        11. create_post:
            method: POST
            url: api/post/create_post/
            func: 創建使用者的文章

        12. update_post:
            method: PUT
            url: api/post/<pk>/update/
            func: 更新文章

        13. delete_post:
            method: DELETE
            url: api/post/<pk>/delete/
            func: 刪除文章

    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'], url_path='counter-data', permission_classes=[])
    def counter_data(self, request):
        '''
            返回計數器數據
        '''
        data = {
            'users_count': User.objects.count(),
            'posts_count': Post.objects.count(),
            'visits_count': Post.objects.aggregate(total_views=Sum('views'))['total_views'] or 0,
            'students_count': Profile.objects.count(),
        }
        return Response(data)

    @action(detail=False, methods=['get'], url_path='all_posts', permission_classes=[])
    def get_all_posts(self, request):
        '''
            取得所有文章
        '''
        sort_by = request.query_params.get('sort_by', '-created_at')  # 默認按創建時間降序排序
        category = request.query_params.get('category', None)
        tag = request.query_params.get('tag', None)
        search = request.query_params.get('search', None)

        posts = Post.objects.all()

        if category:
            posts = posts.filter(category__name=category)
        
        if tag:
            posts = posts.filter(tags__name=tag)
        
        if search:
            posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search) | posts.filter(category__name__icontains=search)

        allowed_sort_fields = ['created_at', 'title', 'views', '-created_at', '-title', '-views', 'likes']
        if sort_by.lstrip('-') not in allowed_sort_fields:
            sort_by = '-created_at'
            
        posts = posts.order_by(sort_by)

        paginator = PostPagination()
        result_page = paginator.paginate_queryset(posts, request)

        if result_page is not None:
            serializer = self.get_serializer(result_page, many=True)
            response_data = serializer.data

            for post_data, post in zip(response_data, result_page):
                post_data['likes'] = post.likes.count()
                post_data['comments'] = post.comments.count()
                post_data['category'] = CategorySerializer(post.category).data

            response = paginator.get_paginated_response(response_data)
            response.data['total_posts'] = posts.count()
            response.data['total_pages'] = paginator.page.paginator.num_pages
            return response

        serializer = self.get_serializer(posts, many=True)
        response_data = serializer.data

        for post_data, post in zip(response_data, posts):
            post_data['likes'] = post.likes.count()
            post_data['comments'] = post.comments.count()
            post_data['category'] = CategorySerializer(post.category).data
        return Response(response_data)
    
    @action(detail=False, methods=['get'], url_path='article/(?P<slug>[^/.]+)', permission_classes=[])
    def get_post_by_slug(self, request, slug=None):
        '''
            取得文章的詳細資訊
        '''
        try:
            post = Post.objects.get(slug=slug)
            
            serializer = self.get_serializer(post)
            post_data = serializer.data
            
            post_data['likes_count'] = post.likes.count()
            post_data['comments_count'] = post.comments.count()
            post_data['tags'] = [tag.name for tag in post.tags.all()]
            post_data['category'] = post.category.name if post.category else None

            user = request.user
            post_data['liked'] = post.liked_by.filter(id=user.id).exists() if user.is_authenticated else False
            

            previous_post = Post.objects.filter(author=post.author, created_at__lt=post.created_at).order_by('-created_at').first()
            next_post = Post.objects.filter(author=post.author, created_at__gt=post.created_at).order_by('created_at').first()

            if not previous_post:
                previous_post = Post.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()
            if not next_post:
                next_post = Post.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()

            post_data['previous_post'] = {
                'title': previous_post.title,
                'slug': previous_post.slug
            } if previous_post else None
            
            post_data['next_post'] = {
                'title': next_post.title,
                'slug': next_post.slug
            } if next_post else None
            
            post_data['comments'] = []

            for comment in post.comments.all():
                comment_data = {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.profile.name if comment.profile.name else comment.profile.user.username,
                    'studinet_id': comment.profile.studient_id if comment.profile.studient_id else comment.profile.user.username,
                    'created_at': comment.created_at
                }
                post_data['comments'].append(comment_data)
    
            return Response(post_data)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['get'], url_path='latest', permission_classes=[])
    def get_latest_posts(self, request):
        '''
            取得最新文章
        '''
        posts = Post.objects.all().order_by('-created_at')[:4]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-tag/(?P<tag_name>[^/.]+)', permission_classes=[])
    def get_posts_by_tag(self, request, tag_name=None):
        '''
            取得標籤名稱為<tag_name>的所有文章
        '''
        posts = Post.objects.filter(tags__name=tag_name)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='details', permission_classes=[IsAuthenticated])
    def get_post_details(self, request):
        '''
            取得文章的詳細資訊
        '''
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(author=profile.user).order_by('-created_at')  # 添加排序

        paginator = PostPagination()
        result_page = paginator.paginate_queryset(posts, request)

        if not result_page:
            return Response({'detail': 'No posts found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = []
        for post in result_page:
            comments_count = post.comments.count()
            likes_count = post.likes.count()
            post_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'views': post.views,
                'comments_count': comments_count,
                'likes_count': likes_count
            }
            data.append(post_data)
        
        response = paginator.get_paginated_response(data)
        response.data['total_posts'] = posts.count()
        response.data['total_pages'] = paginator.page.paginator.num_pages
        return response
    
    @action(detail=True, methods=['get'], url_path='detail', permission_classes=[IsAuthenticated])
    def get_post_detail(self, request, pk=None):
        '''
            取得文章的詳細資訊
        '''
        post = self.get_object()
        comments_count = post.comments.count()
        likes_count = post.likes.count()
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'link': post.link,
            'created_at': post.created_at,
            'comments_count': comments_count,
            'likes_count': likes_count,
            'tags': [tag.name for tag in post.tags.all()],
            'category': post.category.name if post.category else None
        }
        return Response(post_data)

    @action(detail=False, methods=['get'], url_path='leaderboard', permission_classes=[])
    def get_leaderboard(self, request):
        '''
            取得文章的排行榜
        '''
        category = request.query_params.get('category', None)

        if category:
            subquery = Post.objects.filter(
                author_id=OuterRef('author_id'),
                category_id=category
            ).annotate(max_likes=Max('likes')).order_by('-max_likes').values('id')[:1]
        else:
            subquery = Post.objects.filter(
                author_id=OuterRef('author_id'),
            ).annotate(max_likes=Max('likes')).order_by('-max_likes').values('id')[:1]


        posts = Post.objects.filter(
            id__in=Subquery(subquery),
            author__profile__isnull=False,
            author__posts__isnull=False
        ).annotate(likes_count=Count('likes')).order_by('-likes_count')

        serializer = PostSerializer(posts, many=True)
        response_data = serializer.data

        # 加入 profile 資料
        for post_data, post in zip(response_data, posts):
            post_data['profile'] = {
                'id': post.author.profile.id,
                'name': post.author.profile.name,
                'studient_id': post.author.profile.studient_id,
            }
            post_data['likes_count'] = post.likes_count
            post_data['category'] = CategorySerializer(post.category).data

        return Response(response_data)
    
    @action(detail=False, methods=['get'], url_path='export-leaderboard', permission_classes=[])
    def export_leaderboard(self, request):
        '''
            匯出文章排行榜為 CSV
        '''
        subquery = Post.objects.filter(
            author_id=OuterRef('author_id'),
            category_id=OuterRef('category_id')
        ).annotate(max_likes=Max('likes')).order_by('-max_likes').values('id')[:1]
        posts = Post.objects.filter(
            id__in=Subquery(subquery),
            author__profile__isnull=False,
            author__posts__isnull=False
        ).annotate(likes_count=Count('likes')).order_by('-likes_count')

        data = []
        for rank, post in enumerate(posts, start=1):
            data.append({
                '排名': rank,
                '學號': post.author.profile.studient_id,
                '類別': post.category.name,
                '按讚數': post.likes_count,
                '瀏覽量': post.views,
                'PO文日期': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化日期
            })

        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')  # 改用 'utf-8-sig'
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="leaderboard.csv"'
        response.write(csv_data)
        return response
    
    @action(detail=True, methods=['post'], permission_classes=[])
    def like_post(self, request, pk=None):
        '''
            按讚文章
        '''
        post = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({'detail': '尚未登入，請先登入之後再操作', 'likes_count': post.liked_by.count()}, status=status.HTTP_403_FORBIDDEN)

        post_like, created = PostLike.objects.get_or_create(user=user, post=post)
        
        if not created:
            post_like.delete()
            liked = False
        else:
            liked = True
        return Response({'liked': liked, 'likes_count': post.liked_by.count()})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_post(self, request):
        '''
            創建使用者的文章
        '''
        try:
            data = request.data.copy()
            try:
                profile = Profile.objects.get(user=request.user)
                data['studient_id'] = profile.studient_id
            except Profile.DoesNotExist:
                pass

            serializer = self.get_serializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='update', permission_classes=[IsAuthenticated])
    def update_post(self, request, pk=None):
        '''
            更新文章
        '''
        try:
            post = self.get_object()
            serializer = self.get_serializer(post, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete', permission_classes=[IsAuthenticated])
    def delete_post(self, request, pk=None):
        '''
            刪除文章
            method: DELETE
            url: api/post/<pk>/delete/

            return: status.HTTP_204_NO_CONTENT
        '''
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class PostPagination(PageNumberPagination):
    '''
        文章分頁
    '''
    page_size = 4
    
class CategoryView(viewsets.ModelViewSet):
    '''
    1. queryset: 資料庫查詢的資料集
    2. serializer_class: 使用的序列化器為CategorySerializer
    3. permission_classes: 使用的權限類別為登入者才能存取

    function:
        1. create:
            method: POST
            url: api/category/create/
            func: 創建文章分類
            
    '''
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(create_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagView(viewsets.ModelViewSet):
    ''''
    1. queryset: 資料庫查詢的資料集'
    2. serializer_class: 使用的序列化器為TagSerializer
    3. permission_classes: 使用的權限類別為登入者才能存取
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []

class CommentView(viewsets.ModelViewSet):
    '''
    1. queryset: 資料庫查詢的資料集
    2. serializer_class: 使用的序列化器為CommentSerializer
    3. permission_classes: 使用的權限類別為登入者才能存取

    function:
        1. create:
            method: POST
            url: api/comment/create/
            func: 創建留言
        

    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        '''
            創建留言
        '''
        try:
            post = Post.objects.get(id=request.data['post'])
            profile = Profile.objects.get(user=request.user)
            data = request.data.copy()
            data['profile'] = profile.id

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(post=post, profile=profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
