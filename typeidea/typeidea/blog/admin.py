from django.contrib import admin
from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


# Register your models here.
class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = (PostInline,)
    list_display = ('id', 'name', 'status', 'is_nav', 'owner', 'post_count', 'created_time')
    list_display_links = ('id', 'name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('id', 'name', 'status', 'created_time')
    list_display_links = ('id', 'name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('id', 'title', 'status', 'category_name', 'tag_name', 'owner', 'created_time')
    list_display_links = ('id', 'title', 'status', 'category_name', 'tag_name', 'owner', 'created_time')
    list_filter = (CategoryOwnerFilter,)
    search_fields = ('title', 'category__name')

    # 编辑页面
    fieldsets = (
        ('基础配置', {'fields': ('title', 'category', 'status')}),
        ('内容', {'fields': ('desc', 'content')}),
        ('额外信息', {'fields': ('tag',)})
    )

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = '分类'

    def tag_name(self, obj):
        return [x.name for x in obj.tag.all()]

    tag_name.short_description = '标签'

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
