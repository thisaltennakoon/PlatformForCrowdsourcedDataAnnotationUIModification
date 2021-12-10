from django.db import models


class Task(models.Model):
    Title = models.CharField(max_length=200, blank=False)
    Description = models.TextField(max_length=255,blank=True)
    requiredNumofAnnotations = models.IntegerField(default = 1)
    def __str__(self):  # display book name in admin panel
        return self.Title


class DataClass(models.Model):
    TaskID = models.ForeignKey(Task , on_delete=models.CASCADE)
    ClassName = models.CharField(max_length=100, blank=False)
    ClassID = models.IntegerField(default = 0,null=False,blank=False)
    def __str__(self):  # display book name in admin panel
        return self.ClassName


class AnnotationDataSet(models.Model):
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    DataInstance = models.ImageField(upload_to='img',blank=False)
    NumberOfAnnotations = models.IntegerField(default = 0)
    IsViewing = models.BooleanField(default=False)
    WhoIsViewing = models.IntegerField(default = 0,null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)
    def __str__(self):  # display book name in admin panel
        return self.DataInstance.url


