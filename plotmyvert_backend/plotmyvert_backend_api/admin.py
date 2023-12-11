from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *

# Register your models here.
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
      (None, {"fields": ("email", "password", "is_staff", "is_active")}),
      ("Email Settings", {"fields": ("receive_email_login", "receive_email_password", "receive_email_receiver", "mail_server", "mail_port", "mail_SSL")}),
    )
    add_fieldsets = (
      (None, {
        "classes": ("wide",),
        "fields": (
          "email", "password1", "password2", "is_staff",
          "is_active", "groups", "user_permissions",
          "receive_email_login", "receive_email_password", "receive_email_receiver", "mail_server", "mail_port", "mail_SSL"
        )}
      ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, UserAdmin)


@admin.register(JumpSessionModel)
class JumpSessionModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_start_datetime', 'count', 'average_high', 'highest', 'plotly_json')
    search_fields = ('user__email', 'start_datetime')
    list_filter = ('user', 'start_datetime')

    def formatted_start_datetime(self, obj):
        return obj.start_datetime.strftime('%Y-%m-%d %H:%M:%S')
    formatted_start_datetime.admin_order_field = 'start_datetime'
    formatted_start_datetime.short_description = 'Start Datetime'

@admin.register(JumpSessionJumpsModel)
class JumpSessionJumpsModelAdmin(admin.ModelAdmin):
    list_display = ('session', 'formatted_timestamp', 'jump_height')
    search_fields = ('session__start_datetime', 'session__user__email', 'timestamp')
    list_filter = ('session__user', 'timestamp')

    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.admin_order_field = 'timestamp'
    formatted_timestamp.short_description = 'Timestamp'