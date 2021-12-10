from django.shortcuts import render, redirect, reverse
from .models import DataAnnotationResult
from django.http import HttpResponse
#from CreateDataAnnotationTask.models import Task, DataClass, AnnotationDataSet
from CreateTask.models import Task, Cateogary, MediaDataInstance
from .models import DataAnnotationResult
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from UserManagement.models import ContributorTask
from django.db import DatabaseError, transaction

# DataClass = Cateogary , AnnotationDataSet = MediaDataInstance  Task, Task_id, User, User_id, id

def test(request):
    task_id=5
    data_instances = MediaDataInstance.objects.filter(taskID_id=task_id)
    print(data_instances[0].media.url.split('/')[-1])
    return render(request, 'DoTask/test.html', {'data_instances': data_instances})




@login_required(login_url='UserManagement:sign_in')
def task(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        data_class_id = request.POST['data_class_id']
        data_instance = request.POST['DataInstance']
        task_id = request.POST['task_id']
        try:
            with transaction.atomic():
                print(1)
                annotating_data_instance = MediaDataInstance.objects.get(taskID_id=task_id, media=data_instance)
                print(2)
                print(annotating_data_instance)
                if (annotating_data_instance.WhoIsViewing==user_id) and (annotating_data_instance.IsViewing==True) and (annotating_data_instance.NumberOfAnnotations < Task.objects.get(id=task_id).requiredNumofAnnotations):  # for extra protection.Can be removed if nessasary
                    print(3)
                    #print(11)
                    print(Task.objects.get(id=task_id))
                    print(data_instance)
                    print(data_class_id)
                    print(user_id)
                    data_annotation_result = DataAnnotationResult(TaskID=Task.objects.get(id=task_id),
                                                                  DataInstance=data_instance,
                                                                  ClassID=data_class_id,
                                                                  UserID=user_id)
                    print(4)
                    print(data_annotation_result)
                    data_annotation_result.save()
                    print(5)
                    annotating_data_instance.IsViewing = False
                    print(6)
                    annotating_data_instance.WhoIsViewing = 0
                    print(7)
                    annotating_data_instance.NumberOfAnnotations += 1
                    print(8)
                    #print(annotating_data_instance.NumberOfAnnotations)
                    annotating_data_instance.save()
                    print(9)
                    return redirect('/DoTask/Task?task_id=' + str(task_id))
                else:
                    return redirect('/DoTask/Task?task_id=' + str(task_id))
        except DatabaseError:
            return HttpResponse("task Upper DatabaseError")
    else:
        try:
            task_id = request.GET['task_id']
            task=Task.objects.get(id=task_id)
            task_type = task.taskType
            data_instance_annotation_times = int(task.requiredNumofAnnotations)
            annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
            #print(annotated_data_instances)
            data_instances_to_exclude = []
            for i in annotated_data_instances:
                data_instances_to_exclude += [i.DataInstance]
            try:
                skip_instance=request.GET['skip_instance']
                data_instances_to_exclude += [skip_instance]
                skip_instance_request =True
            except:
                skip_instance_request =False
            try:
                with transaction.atomic():
                    data_annotation = MediaDataInstance.objects.filter(taskID_id=task_id,IsViewing=False,NumberOfAnnotations__lt=data_instance_annotation_times).exclude(media__in=data_instances_to_exclude)
                    #print(data_annotation)
                    if len(data_annotation) > 0:
                        data_instance = random.choice(data_annotation)
                        #print(data_instance)
                        data_instance_about_to_annotate = MediaDataInstance.objects.get(taskID_id=task_id, media=data_instance.media)
                        #print(data_instance_about_to_annotate)
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        #print(Cateogary.objects.filter(taskID_id=task_id))
                        #print(task_id)
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    elif len(data_annotation)==0 and skip_instance_request:
                        data_instance = skip_instance
                        data_instance_about_to_annotate = MediaDataInstance.objects.get(taskID_id=task_id, media=data_instance.media)
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    else:
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTask/Task.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False,})
            except DatabaseError:
                print('below database error')
                return HttpResponse("task below DatabaseError")
        except:
            return HttpResponse('last error')
            #return redirect('/DoTask/')

@login_required(login_url='UserManagement:sign_in')
def skip_data_instance(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                if stop_viewing(request,task_id,viewing_data_instance):
                    return redirect('/DoTask/Task?skip_instance='+viewing_data_instance+'&task_id=' + str(task_id))
                else:
                    return HttpResponse('error')
        except DatabaseError:
            return HttpResponse("skip_data_instance DatabaseError")
    except:
        return redirect('/DoTask/Task?task_id=' + str(task_id))

@login_required(login_url='UserManagement:sign_in')
def stop_contributing(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        if stop_viewing(request,task_id,viewing_data_instance):
            return redirect('/DoTask/')
        else:
            return HttpResponse('error')
    except:
        return redirect('/DoTask/')

@login_required(login_url='UserManagement:sign_in')
def stop_viewing(request,task_id,viewing_data_instance):
    try:
        task_id = task_id
        viewing_data_instance = viewing_data_instance
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                annotating_data_instance = MediaDataInstance.objects.get(taskID_id=task_id,media=viewing_data_instance)
                if (annotating_data_instance.WhoIsViewing == user_id) and (annotating_data_instance.IsViewing == True):
                    annotating_data_instance.IsViewing = False
                    annotating_data_instance.WhoIsViewing = 0
                    annotating_data_instance.save()
                    return True
        except DatabaseError:
            return False
    except:
        return False


@login_required(login_url='UserManagement:sign_in')
def view_my_contributions(request):
    try:
        task_id = request.GET['task_id']
        user_id = request.session['user_id']
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
        if len(annotated_data_instances) > 0:
            return render(request, 'DoTask/ViewMyAnnotations.html', {'annotated_data_instances_available': True,
                                                               'task_object': Task.objects.get(id=task_id),
                                                               'annotated_data_instances':annotated_data_instances},)
        else:
            return render(request, 'DoTask/ViewMyAnnotations.html', {'annotated_data_instances_available': False,
                                                               'task_object': Task.objects.get(id=task_id), })
    except:
        return redirect('/DoTask/')

@login_required(login_url='UserManagement:sign_in')
def view_my_contributions_change(request):
    if request.method == 'POST':
        annotated_data_instance_id = request.POST['annotated_data_instance_id']
        data_class_id = request.POST['data_class_id']
        data_annotation_result_not_updated = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = data_annotation_result_not_updated.TaskID_id
        data_annotation_result_not_updated.ClassID = data_class_id
        data_annotation_result_not_updated.save()
        return redirect('/DoTask/ViewMyAnnotations?task_id=' + str(task_id))
    else:
        annotated_data_instance_id = request.GET['annotated_data_instance_id']
        annotated_data_instance = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = annotated_data_instance.TaskID_id
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        data_instance = MediaDataInstance.objects.get(taskID_id= task_id ,media = annotated_data_instance.media)
        return render(request, 'DoTask/ViewMyAnnotationsChange.html',{'annotated_data_instance':annotated_data_instance,
                                                                                    'annotated_data_instance_id':annotated_data_instance_id,
                                                                                     'data_instance':data_instance,
                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                     'data_classes': Cateogary.objects.filter(taskID_id=task_id),})

"""def view_my_annotations_delete(request):
    annotated_data_instance_id = request.GET['annotated_data_instance_id']
    task_id = DataAnnotationResult.objects.get(id=annotated_data_instance_id).TaskID_id
    try:
        last_confirmation = request.GET['last_confirmation']
        if last_confirmation=="True":
            DataAnnotationResult.objects.get(id=annotated_data_instance_id).delete()
            return redirect('/DoTask/ViewMyAnnotations?task_id='+str(task_id))
        else:
            return redirect('/DoTask/ViewMyAnnotations/Change?annotated_data_instance_id=' + str(annotated_data_instance_id))

    except:
        return render(request, 'DoTask/ViewMyAnnotationsDelete.html', {'annotated_data_instance_id': annotated_data_instance_id,
                                                                                     'task_object':Task.objects.get(id=task_id)})"""
