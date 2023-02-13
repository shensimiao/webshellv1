from django.contrib import admin
from .models import Device, Script, Setting


# Register your models here.


@admin.register(Device)
class deviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_name', 'device_passwd', 'device_host', 'device_user',
                    'device_port', 'device_type', 'last_updated')


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'script_name', 'script_reson', 'device_type', 'last_updated')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'setting_name', 'setting_value')


# 在admin中注册绑定
# admin.site.register(device, deviceAdmin)
#
# admin.site.register(Script, ScriptAdmin)
#
# admin.site.register(Setting, SettingAdmin)
