from django.db import models


# Create your models here.
class Drvice(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    drvice_name = models.CharField(max_length=100, default='')
    drvice_passwd = models.CharField(max_length=100, default='')
    drvice_host = models.CharField(max_length=100, default='')
    drvice_user = models.CharField(max_length=100, default='')
    drvice_port = models.IntegerField(default=22)
    drvice_type = models.CharField(max_length=100, default='')
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'Drvice'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return "<Drvice(id={}, drvice_name={}, drvice_passwd={}, drvice_user={}," \
               " drvice_host={}, drvice_port={}, drvice_type={}, last_updated={})>".format(
            self.id, self.drvice_name, self.drvice_passwd, self.drvice_user, self.drvice_host,
            self.drvice_port, self.drvice_type, self.last_updated
        )


class Script(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    drvice_type = models.CharField(max_length=10000)
    script_name = models.CharField(max_length=100)
    script_reson = models.CharField(max_length=10000)
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'drvice_script'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return "<Script(id={}, drvice_type={}, script_name={}, script_reson={}," \
               " last_updated={})>".format(
            self.id, self.drvice_type, self.script_name, self.script_reson, self.last_updated
        )


class Setting(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    setting_name = models.CharField(max_length=100, default='')
    setting_value = models.CharField(max_length=1000, default='')

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.setting_value

