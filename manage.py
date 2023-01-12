#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import models


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webshell.conf.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# def NotFoundSetting(param):
#     pass
#
#
class Drvice(models.Model):
    # __table_args__ = {'comment': '存放路由器配置'}
    id = models.IntegerField(primary_key=True, auto_created=True)
    drvice_name = models.CharField(max_length=100)
    _drvice_passwd = models.CharField(max_length=100)
    drvice_host = models.CharField(max_length=100)
    drvice_port = models.IntegerField
    drvice_type = models.CharField(max_length=100)
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'drvice_tables'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.drvice_name


class Script(models.Model):
    __table_args__ = {'comment': '存放路由器脚本'}
    id = models.IntegerField(primary_key=True, auto_created=True)
    drvice_type = models.ForeignKey(Drvice, on_delete=models.DO_NOTHING, verbose_name='drvice_type', blank=True)
    script_name = models.CharField(max_length=100)
    script_reson = models.CharField(max_length=10000)
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'drvice_script'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.script_reson


if __name__ == '__main__':
    main()
