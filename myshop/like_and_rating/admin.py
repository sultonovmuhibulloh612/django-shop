from django.contrib import admin
from .models import ProductLike, ProductReview

@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']
    list_display_links = ['id', 'user']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'product__name']
    raw_id_fields = ['user', 'product']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'product')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    # В списке показываем все поля, но редактировать можно только is_active
    list_display = ['id', 'user', 'product', 'rating', 'short_comment', 'is_active', 'created_at']
    list_display_links = ['id', 'user']  # По id и user можно перейти к редактированию
    list_editable = ['is_active']  # Только is_active можно редактировать прямо в списке
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'product__name', 'comment']
    date_hierarchy = 'created_at'
    
  
    readonly_fields = ['user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
   
    fieldsets = (
        (None, {
            'fields': ('user', 'product', 'rating')
        }),
        ('Review', {
            'fields': ('comment',),
            'classes': ('wide',)
        }),
        ('Moderation', {
            'fields': ('is_active',),  
            'classes': ('wide',),
            'description': 'Только поле "Активность" доступно для изменения'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def short_comment(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    short_comment.short_description = 'Comment'
    
   
    def has_add_permission(self, request):
        return False
    

    def has_delete_permission(self, request, obj=None):
        return True
    
   