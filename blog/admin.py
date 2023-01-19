from django.contrib import admin
from .models import Drvice, Script, Setting


# Register your models here.


@admin.register(Drvice)
class DrviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'drvice_name', 'drvice_passwd', 'drvice_host', 'drvice_user',
                    'drvice_port', 'drvice_type', 'last_updated')


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'script_name', 'script_reson', 'drvice_type', 'last_updated')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'setting_name', 'setting_value')


# 在admin中注册绑定
# admin.site.register(Drvice, DrviceAdmin)
#
# admin.site.register(Script, ScriptAdmin)
#
# admin.site.register(Setting, SettingAdmin)
