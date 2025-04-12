from django.contrib import admin
from .models import User, Course, Document, Download, Login, Rating

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'phone')
	search_fields = ('name', 'phone')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'code')
	search_fields = ('name', 'code')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'uploaded_by', 'course', 'views', 'downloads', 'upload_date')
	search_fields = ('title', 'term')
	list_filter = ('course', 'term')

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'document', 'timestamp', 'ip')
	search_fields = ('user__name', 'document__title', 'ip')
	list_filter = ('timestamp',)

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'login_time', 'ip')
	search_fields = ('user__name', 'ip')
	list_filter = ('login_time',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'document', 'score', 'timestamp')
	search_fields = ('user__name', 'document__title')
	list_filter = ('score', 'timestamp')

