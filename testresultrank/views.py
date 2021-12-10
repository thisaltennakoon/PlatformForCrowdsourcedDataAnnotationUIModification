from django.contrib.auth import get_user_model
from django.shortcuts import render
from UserManagement.models import Profile as User1
from CreateTask.models import Task , AnnotationTest, TestResult
from DoDataAnnotationTask.models import DataAnnotationResult as imganre
from DoTextDataAnnotationTask.models import DataAnnotationResult as txtanre
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
import random
import json


#def first(request):
 #   user = Task.objects.get(id=1)
  #  return render(request, 'analyse/viewresult.html', {'user': user})


def resultanalyse(request):
    TaskID = request.GET['Task_ID']
    re = TestResult.objects.filter(testID_id=TaskID).order_by('score')
    result = []
    annotator = []
    annotator_name = []
    task = []
    lenth = []
    for j in re.reverse():
        result.append(float(j.score))
        annotator.append(j.annotatorID_id)
    for i in annotator:
        user = User1.objects.get(id=i)
        annotator_name.append(user.first_name + " " + user.last_name)
        donetask = txtanre.objects.filter(UserID=i)
        doneimgtask = imganre.objects.filter(UserID=i)
        lk = []
        lki = []

        for l in donetask:
            lk.append(l.TaskID_id)
        for li in doneimgtask:
            lki.append(li.TaskID_id)
        seen = set()
        uniq = []
        for x in lk:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
        seeni = set()
        uniqi = []
        for y in lki:
            if y not in seeni:
                uniqi.append(y)
                seeni.add(y)
        titt = []
        for tit in uniq:
            tit2 = Task.objects.filter(id=str(tit)).values('title')
            titt.append(tit2[0]['title'])
        for titi in uniqi:
            tit2i = Task.objects.filter(id=str(titi)).values('title')
            titt.append(tit2i[0]['title'])
        lenth.append(len(titt))
        task.append(titt)

    context = {'categories': annotator_name, 'values': result, 'task': task, 'le': lenth}
    return render(request, 'analyse/index.html', context=context)