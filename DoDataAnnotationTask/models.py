from django.db import models
from CreateTask.models import Task,MediaDataInstance


class DataAnnotationResult(models.Model):
    TaskID = models.ForeignKey(Task ,related_name='imageanno', on_delete=models.CASCADE)
    DataInstance = models.ForeignKey(MediaDataInstance , on_delete=models.CASCADE)
    ClassID = models.IntegerField(default=0, null=False, blank=False)
    UserID = models.IntegerField(null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)
