from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from myApp.models import Project, PBI, PickedPBI, Task, Developer
from myApp.forms import PBIForm, SprintUpdateForm
from bootstrap_modal_forms.generic import (BSModalUpdateView, BSModalDeleteView, BSModalCreateView)
from django.views.generic import ListView
from django.http import HttpResponseRedirect


# Create your views here.
# random

class ProductOwnerViewCurrent(ListView):
    template_name = 'PBI_list.html'
    model = PBI
    ordering = ['priority']

    def priority_up_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        upid = request.POST.get('upid', '')
        obj = PBI.objects.filter(id=myid).first()
        obj1 = PBI.objects.filter(id=upid).first()
        # for obj in objs:
        temp = obj.priority
        temp1 = obj1.priority
        obj.priority = -1
        obj.save()
        obj1.priority = temp
        obj1.save()
        obj.priority = temp1
        obj.save()
        context = {
        'object': obj
        }
        # return HttpResponseRedirect('/myApp/pbis')
        return render(request, 'PBI_list.html', {})

    def priority_down_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        downid = request.POST.get('downid', '')
        obj = PBI.objects.filter(id=myid).first()
        obj1 = PBI.objects.filter(id=downid).first()
        # for obj in objs:
        temp = obj.priority
        temp1 = obj1.priority
        obj.priority = -1
        obj.save()
        obj1.priority = temp
        obj1.save()
        obj.priority = temp1
        obj.save()
        context = {
        'object': obj
        }
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def status_change_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        newStatus = request.POST.get('newStatus', '')
        obj = PBI.objects.filter(id=myid).first()
        obj.status =  newStatus
        obj.save()
        context = {
        'object': obj
        }
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def pbi_delete_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        obj = PBI.objects.filter(id=myid).first()
        mypriority = obj.priority
        obj.delete()
        others = PBI.objects.all()
        for other in others:
            if (other.priority and other.priority > mypriority):
                other.priority = (other.priority - 1)
                other.save()
        context = {
        }
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def priority_auto_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        obj = PBI.objects.filter(id=myid).first()
        # for obj in objs:
        obj.priority = obj.priority - 1
        obj.save()
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def process_done_view(request):
        myid = request.POST.get('myid', '')
        obj = PBI.objects.filter(id=myid).first()
        mypriority = obj.priority
        obj.priority = None
        obj.status = 3
        obj.save()
        others = PBI.objects.all()
        for other in others:
            if other.priority != None and mypriority != None:
                if other.priority > mypriority:
                    other.priority = (other.priority - 1)
                    other.save()
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

class ProductOwnerViewAll(ListView):
    template_name = 'PBI_fullList.html'
    model = PBI
    ordering = ['name']


class PBICreateView(BSModalCreateView):
    model = PBI
    template_name = 'modalPage/PBI_create.html'
    form_class = PBIForm
    success_message = 'Success: PBI was created.'
    success_url = reverse_lazy('all_pbis')

class PBIDetailView(BSModalUpdateView):
    model = PBI
    template_name = 'modalPage/PBI_detail.html'
    form_class = PBIForm
    success_message = 'Success: PBI was updated.'
    success_url = reverse_lazy('all_pbis')

class PBIRealDetailView(BSModalUpdateView):
    model = PBI
    template_name = 'modalPage/PBI_realdetail.html'
    form_class = PBIForm
    success_message = 'Success: PBI was updated.'
    success_url = reverse_lazy('pbi_list')

class PBIDeleteView(BSModalDeleteView):
    model = PBI
    template_name = 'modalPage/PBI_delete.html'
    success_message = 'Success: PBI was deleted.'
    success_url = reverse_lazy('pbi_list')

## Views for sprint backlog functions
class SprintBacklog(TemplateView):
    template_name = "sprintBacklog.html"

    def get_context_data(self, **kwargs):
        # owner = self.kwargs['Users']

        context = super().get_context_data(**kwargs)

        #temp project value before the authentication is inplaced.
        project = Project.objects.get(pk=1)
        pbis = PickedPBI.objects.order_by('pbi__name').all()
        tasks = Task.objects.all()
        pbisToBePulled = PBI.objects.filter(status=1) | PBI.objects.filter(status=4)
        notStarted = []
        inProgress = []
        done = []
        pullItems  = []
        taskNum = []
        for pbi in pbis:
            taskNum.append(0);
        for task in tasks:
            i = 0
            for pbi in pbis:
                if task.pbiPicked == pbi:
                    taskNum[i] = taskNum[i] + 1 
                    if task.status == 1:
                        notStarted.append(task)
                    elif task.status == 2:
                        inProgress.append(task)
                    elif task.status == 3:
                        done.append(task)
                    break
                i = i + 1
        for pbiToBePulled in pbisToBePulled:
            notPulled = True
            for picked in pbis:
                if picked.pbi == pbiToBePulled:
                    notPulled = False
                    break
            if notPulled == True:
                pullItems.append(pbiToBePulled)

        context['project'] = project
        context['pbis'] = PickedPBI.objects.order_by('pbi__name').all()
        context['notStartedTasks'] = notStarted
        context['inProgressTasks'] = inProgress
        context['doneTasks'] = done
        context['pullItems'] = pullItems
        context['taskNum'] = taskNum
        return context

    def pull_task_view(request):
        pbiid = request.POST.get('pbiid', '')
        obj = PBI.objects.filter(id=pbiid).first()
        pulledTask = PickedPBI(pbi = obj)
        pulledTask.save()
        obj.status = 2
        obj.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def deletePulled(request):
        pbiid = request.POST.get('pbiid', '')
        obj = PickedPBI.objects.filter(id=pbiid).first()
        pbi = obj.pbi
        obj.delete()
        pbi.status = 4
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def clear(request):
        projectid = request.POST.get('projectid', '')
        project = Project.objects.get(pk=projectid)
        pbis = []
        pickedPbis = PickedPBI.objects.all()
        for pbi in pickedPbis:
            if pbi.pbi.project == project:
                pbis.append(pbi.pbi)
                pbi.delete()
        others = PBI.objects.all()
        for pbi in pbis:
            pbi.status = 3
            mypriority = pbi.priority
            pbi.priority = None
            pbi.save()
            for other in others:
                if other.priority != None and mypriority != None:
                    if other.priority > mypriority:
                        other.priority = (other.priority - 1)
                        other.save()
        project.sprint = project.sprint + 1
        project.sprintEffort = 0
        project.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

class SprintUpdateView(BSModalUpdateView):
    model = Project
    template_name = 'modalPage/sprintUpdate.html'
    form_class = SprintUpdateForm
    success_message = 'Success: PBI was updated.'
    success_url = reverse_lazy('sprint_backlog')


class taskDetails(TemplateView):
    template_name = "taskDetails.html"

    def get_context_data(self, **kwargs):
        task = self.kwargs['task']

        context = super().get_context_data(**kwargs)

        tasks = Task.objects.get(pk = task)
        
        context['task'] = tasks

        return context

    def edit(request):
        taskid = request.POST.get('taskid', '')
        task = Task.objects.get(pk=taskid)
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        estimate = request.POST.get('estimate', '')
        # status = request.POST.get('status', '')
        task.name = name
        task.Description = description
        task.estimate = estimate
        # task.status = status
        task.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def pick(request):
        taskid = request.POST.get('taskid', '')
        task = Task.objects.get(pk=taskid)
        devid = request.POST.get('devid', '')
        dev = Developer.objects.get(pk=devid)
        pbiid = request.POST.get('pbiid', '')
        pbi = PickedPBI.objects.get(pk=pbiid)
        task.pic = dev
        task.status = 2
        pbi.notYetStarted = pbi.notYetStarted - 1
        pbi.inProgress = pbi.inProgress + 1
        task.save()
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def changeStatus(request):
        taskid = request.POST.get('taskid', '')
        task = Task.objects.get(pk=taskid)
        pbiid = request.POST.get('pbiid', '')
        pbi = PickedPBI.objects.get(pk=pbiid)
        status = request.POST.get('status', '')
        if task.status == 2:
            pbi.inProgress = pbi.inProgress - 1
        if task.status == 3:
            pbi.done = pbi.done -1
        task.status = status
        if status == '1':
            task.pic = None
            pbi.notYetStarted = pbi.notYetStarted + 1
        if status == '2':
            pbi.inProgress = pbi.inProgress + 1
        if status == '3':
            pbi.done = pbi.done + 1
        task.save()
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def changeComplete(request):
        estimate = request.POST.get('estimate', '')
        taskid = request.POST.get('taskid', '')
        task = Task.objects.get(pk=taskid)
        complete = request.POST.get('complete','')
        task.complete = complete
        task.estimate = estimate
        task.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def delete(request):
        taskid = request.POST.get('taskid', '')
        pbiid = request.POST.get('pbiid', '')
        task = Task.objects.get(pk=taskid)
        pbi = PickedPBI.objects.get(pk=pbiid)
        task.delete()
        pbi.notYetStarted = pbi.notYetStarted - 1
        pbi.taskNum = pbi.taskNum - 1
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

class taskCreation(TemplateView):
    template_name = "taskCreation.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        pickedPbi = PickedPBI.objects.all()
        context['pbis'] = pickedPbi

        return context

    def create(request):
        pbiid = request.POST.get('pbi', '')
        pbi = PickedPBI.objects.get(pk=pbiid)
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        estimate = request.POST.get('estimate', '')
        addedTask = Task(pbiPicked  = pbi, name = name, Description = description, estimate = estimate)
        addedTask.save()
        pbi.taskNum = pbi.taskNum + 1
        pbi.notYetStarted = pbi.notYetStarted + 1
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))
