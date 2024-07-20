from django.db import models
from django.db import models

class Uploadmp4(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    files = models.FileField(upload_to='files',null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,default=None,null=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField()
