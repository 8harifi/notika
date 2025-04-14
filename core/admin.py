from django.contrib import admin
from .models import User, Course, Document, Download, Login, Rating, Favorite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'code')
	search_fields = ('name', 'code')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'uploaded_by', 'course', 'views', 'downloads', 'upload_date')
	search_fields = ('title', 'description')
	list_filter = ('course', 'description')

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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'added_on')
    search_fields = ('user__email', 'document__title')
    list_filter = ('added_on',)

