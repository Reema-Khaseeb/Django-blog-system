""" Automatic admin interface site for the website """
from django.contrib import admin, messages

from .models import Post, Comment


class CommentInline(admin.TabularInline):
   """ Edit comment model as a parent model """
   model = Comment
   extra = 1


class BlogAdmin(admin.ModelAdmin):
   """ Customizing the Blog Admin interface """
   fieldsets = [
        (None,               {'fields': ['title', 'slug', 'body', 'author', 'status']}),
        ('Date information', {'fields': ['published_at']}),]
   inlines = [CommentInline]
   # Automatically generate the value for Slug field from title field
   prepopulated_fields = {"slug": ("title",)}
   list_display = ('title', 'body', 'slug', 'author',
   'created', 'published_at', 'updated', 'status')
   search_fields = ('title', 'body')
   list_filter = ('published_at',)


class CommentAdmin(admin.ModelAdmin):
   """ Customizing the Comment Admin interface """
   list_display = ['name', 'body', 'post', 'email',
   'created_at', 'active']

   def save_model(self, request, obj, form, change):
      try:
         super().save_model(request, obj, form, change)
      except ValueError:
         self.message_user(request, "you need to wait for 30s.", messages.ERROR)

admin.site.register(Post, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
