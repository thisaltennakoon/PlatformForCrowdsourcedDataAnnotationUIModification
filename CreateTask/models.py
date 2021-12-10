from django.db import models
from django.urls import reverse
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User
#from zipfile import ZipFile


"""class UserNew2(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=64)"""


# IMAGE ANNOTATION AND 'DATA GENARATION'

class Task(models.Model):
    creatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=60, default='inprogress')  # new,#inprogress,#completed
    instructions = models.CharField(max_length=1000)
    field = models.CharField(max_length=30, default='')
    taskType = models.CharField(max_length=10)  # TextAnno,ImgAnno,TextGen,ImgGen
    requiredNumofAnnotations = models.IntegerField(default=1)

    def __str__(self):  
        return self.title


class Cateogary(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    cateogaryName = models.CharField(max_length=250)
    cateogaryTag = models.IntegerField(default=0)  # 0,1,2,..


def directory_path2(instance, filename):
    return 'MediaAnno/task_{0}/{1}'.format(instance.taskID.id, filename)


class MediaDataInstance(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    media = models.FileField(upload_to=directory_path2)
    NumberOfAnnotations = models.IntegerField(default = 0)
    IsViewing = models.BooleanField(default=False)
    WhoIsViewing = models.IntegerField(default = 0,null=False,blank=False)
    LastUpdate = models.DateTimeField()


# TEXT ANNOTATIONS
def directory_path(instance, filename):
    return 'TextAnno/task_{0}/{1}'.format(instance.taskID.id, filename)


class TextFile(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    csvFile = models.FileField(upload_to=directory_path)


class TextDataInstance(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    NumberOfAnnotations = models.IntegerField(default = 0)
    IsViewing = models.BooleanField(default=False)
    WhoIsViewing = models.IntegerField(default = 0,null=False,blank=False)
    LastUpdate = models.DateTimeField()


class TextData(models.Model):
    InstanceID = models.ForeignKey(TextDataInstance, on_delete=models.CASCADE)
    Data = models.CharField(max_length=3000)

#TEXT GENERATION

def directory_path4(instance,filename):
    return 'TextGen/task_{0}/{1}'.format(instance.taskID.id, filename)

class GenTextFile(models.Model):
    taskID = models.ForeignKey(Task,on_delete=models.CASCADE)
    csvFile = models.FileField(upload_to=directory_path)

class DataGenTextInstance(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    data = models.CharField(max_length= 5000)


# QUIZ
class Questionaire(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Active')  # ative,#notactive


class McqQuestion(models.Model):
    questionaireID = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)


class DescrptiveQuestion(models.Model):
    questionaireID = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)


class McqOption(models.Model):
    questionID = models.ForeignKey(McqQuestion, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)


# class DataSetImage(models.Model):
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="uploads", height_field=None, width_field=None, max_length=None)


# class ExampleImage(models.Model):
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='examples', verbose_name='Image')

# class ExampleResults(models.Model):
#     imageID = models.ForeignKey(ExampleImage, on_delete=models.CASCADE)
#     cateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)

# class GenerationTask(models.Model):
#     creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.CharField(max_length=1000)
#     status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
#     instructions = models.CharField(max_length=1000)


# class GenerationClass(models.Model):
#     TaskID = models.ForeignKey(GenerationTask,on_delete=models.CASCADE)
#     classtitle = models.CharField(max_length=1000)
#     requiredDataType = models.CharField(max_length=1,default='T') #Text:T or image:I dont need?

# class GenerationExamplesText(models.Model):
#     ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
#     example = models.CharField(max_length=2000)

# class GenerationExamplesImage(models.Model):
#     ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
#     example = models.ImageField()


# TEXT DATA ANNOTATION

# class TextTask(models.Model):
#     creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.CharField(max_length=1000)
#     status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
#     instructions = models.CharField(max_length=1000)
#     #csvFile = models.FileField(upload_to=directory_path)


# class TextCateogary(models.Model):
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     cateogaryName = models.CharField(max_length= 250)


# TEXT AND MEDIA DATA EXAMPLE AND TEST
class CateogaryTag(models.Model):
    CateogaryID = models.ForeignKey(Cateogary, on_delete=models.CASCADE)
    TagNumber = models.IntegerField()


class AnnotationTest(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)   #0=non_active , 1=active
    required_marks = models.IntegerField(default=50)
    #add pass marks

class TestResult(models.Model):
    testID = models.ForeignKey(AnnotationTest, on_delete=models.CASCADE)
    annotatorID = models.ForeignKey(User, on_delete=models.CASCADE)  # user janani's user table
    score = models.DecimalField(max_digits=5, decimal_places=2)  # score out of 100



# TEXT
def directory_path5(instance, filename):
    return 'TextAnno/Test/task_{0}/{1}'.format(instance.taskID.id, filename)
class TestTextFile(models.Model):                   #To upload example csv file
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    csvFile = models.FileField(upload_to=directory_path5)

class ExampleTextDataInstance(models.Model):
    testID = models.ForeignKey(AnnotationTest, on_delete=models.CASCADE)


class ExampleTextData(models.Model):
    InstanceID = models.ForeignKey(ExampleTextDataInstance, on_delete=models.CASCADE)
    Data = models.CharField(max_length=3000)


class ExampleTextAnnoResult(models.Model):
    ExampleTextDataInstanceID = models.ForeignKey(ExampleTextDataInstance, on_delete=models.CASCADE)
    resultCateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)


class TextAnnoAnswers(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    textInstance = models.ForeignKey(ExampleTextDataInstance, on_delete=models.CASCADE)
    answerCateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)


# MEDIA
def directory_path3(instance, filename):
    return 'MediaAnno/test/task_{0}/{1}'.format(instance.testID.id, filename)


class ExampleMediaDataInstance(models.Model):
    testID = models.ForeignKey(AnnotationTest, on_delete=models.CASCADE)
    mediaData = models.FileField(upload_to=directory_path3)


class ExampleMediaAnnoResult(models.Model):
    ExampleMediaDataInstanceID = models.ForeignKey(ExampleMediaDataInstance, on_delete=models.CASCADE)
    resultCateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)


class MediaAnnoAnswers(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    mediaInstance = models.ForeignKey(ExampleMediaDataInstance, on_delete=models.CASCADE)
    answerCateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)