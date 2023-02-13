from django.db import models


# Create your models here.
class device(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    device_name = models.CharField(max_length=100, default='')
    device_passwd = models.CharField(max_length=100, default='')
    device_host = models.CharField(max_length=100, default='')
    device_user = models.CharField(max_length=100, default='')
    device_port = models.IntegerField(default=22)
    device_type = models.CharField(max_length=100, default='')
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'device'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return "<device(id={}, device_name={}, device_passwd={}, device_user={}," \
               " device_host={}, device_port={}, device_type={}, last_updated={})>".format(
            self.id, self.device_name, self.device_passwd, self.device_user, self.device_host,
            self.device_port, self.device_type, self.last_updated
        )


class Script(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    device_type = models.CharField(max_length=10000)
    script_name = models.CharField(max_length=100)
    script_reson = models.CharField(max_length=10000)
    last_updated = models.DateTimeField

    class Meta:
        verbose_name = 'device_script'
        verbose_name_plural = verbose_name

    def __repr__(self):
        return "<Script(id={}, device_type={}, script_name={}, script_reson={}," \
               " last_updated={})>".format(
            self.id, self.device_type, self.script_name, self.script_reson, self.last_updated
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

