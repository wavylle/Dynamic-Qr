from django.db import models

class userData(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    first_name = models.CharField(max_length = 255, default = 0)
    last_name = models.CharField(max_length = 255, default = 0)
    phone = models.CharField(max_length = 255, default = 0)
    upiid = models.CharField(max_length = 255, default = 0)
    phone_verification_status = models.CharField(max_length = 255, default = False)

    def __str__(self):
        return self.username

class qrRecords(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    timestamp = models.CharField(max_length = 255, default = 0)

    def __str__(self):
        return self.username
