from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.utils import timezone

from .models import DiagnosisHistory, ErrorReport, Feedback, User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'role')


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'fullname', 'role', 'is_active', 'is_staff', 'deleted_at', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'fullname')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'deleted_at', 'terms_accepted_at', 'terms_version')
    actions = ['anonymize_users']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Thông tin', {'fields': ('fullname', 'role')}),
        ('Quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Điều khoản', {'fields': ('terms_accepted_at', 'terms_version')}),
        ('Thời gian', {'fields': ('last_login', 'created_at', 'updated_at', 'deleted_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'role', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            # Tài khoản do admin tạo không qua màn hình đăng ký
            obj.terms_accepted_at = timezone.now()
            obj.terms_version = settings.TERMS_VERSION
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Không xóa thật -> dùng action "Ẩn danh hóa"
        return False

    @admin.action(description='Ẩn danh hóa (xóa tài khoản)')
    def anonymize_users(self, request, queryset):
        users = queryset.filter(deleted_at__isnull=True)
        for user in users:
            user.anonymize()
        self.message_user(request, f'Đã ẩn danh hóa {len(users)} tài khoản.')


@admin.register(DiagnosisHistory)
class DiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'severity', 'infected_ratio', 'lesion_count', 'is_bookmarked', 'created_at')
    list_filter = ('status', 'severity')
    search_fields = ('user__email',)
    list_select_related = ('user',)
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'history', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    list_select_related = ('history',)
    raw_id_fields = ('history',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_resolved', 'created_at')
    list_filter = ('is_resolved',)
    search_fields = ('title', 'description')
    list_select_related = ('user',)
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
