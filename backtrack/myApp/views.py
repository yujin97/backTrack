from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from myApp.models import Project, PBI, PickedPBI, Task, User, invitedDev, invitedScrumMaster
from myApp.forms import PBIForm, SprintUpdateForm
from bootstrap_modal_forms.generic import (BSModalUpdateView, BSModalDeleteView, BSModalCreateView)
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

@login_required
def loginRoute(request):
    if request.user.is_developer:
        if request.user.is_productOwner:
            return ProductOwnerViewCurrent.as_view(projectId=request.user.project.all().first().pk)(request)
        elif request.user.is_devTeam:
            return NonProductOwnerViewCurrent.as_view(projectId=request.user.project.all().first().pk)(request)
        else:
            return DevLoginNoProject.as_view()(request)
    elif request.user.is_manager:
        return ScrumMasterPbList.as_view()(request)

@login_required
def projectCreation(request):
    if request.user.is_developer:
        if request.user.is_productOwner == False and request.user.is_devTeam == False:
            return render(request,'projectCreation.html')

@login_required
def projectCreationOperation(request):
    if request.user.is_developer:
        if request.user.is_productOwner == False and request.user.is_devTeam == False:
            user = request.user
            name = request.POST.get('name','')
            newProject = Project(title=name)
            newProject.save()
            user.project.add(newProject)
            user.productOwner = True
            user.save()
            return HttpResponseRedirect(reverse_lazy('pbi_list'))

@login_required
def inviteDevTeam(request):
    if request.user.is_developer:
        if request.user.is_productOwner == True:
            return render (request, 'inviteDevTeam.html')

@login_required
def inviteDevTeamOperation(request):
    if request.user.is_developer:
        if request.user.is_productOwner == True:
            email = request.POST.get('address','')
            user = User.objects.filter(email= email)
            if user:
                invitation = invitedDev.objects.filter(Q(user=user.first()) & Q(project=request.user.project.all().first()))
                project = user.first().project.all()
                if invitation:
                    data = {'msg': 'The user is already invited to this project', 'go': False}
                    return JsonResponse(data,safe = False)
                elif user.first().is_developer == False:
                    data = {'msg': 'The user is not a developer, hence cannot be added as developement team member', 'go': False}
                    return JsonResponse(data,safe = False)
                elif project:
                    data = {'msg': 'The user is in another project', 'go': False}
                    return JsonResponse(data,safe = False)
                else: 
                    data = {'msg': 'can add', 'go': True}
                    addUser = user.first()
                    addProject = request.user.project.all().first()
                    addInvitation = invitedDev(user=addUser, project = addProject)
                    addInvitation.save()
                    title = f'backTrack Invitation from the project {addProject.title}'
                    content = f'Please click the link below to join the project: localhost:8000/myApp/acceptDevTeam/{addProject.pk}'
                    host = 'hku.backtrack@gmail.com'
                    recipients = [addUser.email,]
                    send_mail(title,
                        content,
                        host,
                        recipients,
                        fail_silently=False)
                    return JsonResponse(data,safe = False)
            else:
                data = {'msg': 'User does not exist!'}
                return JsonResponse(data,safe = False)

@login_required
def acceptDevTeam(request,projectId):
    acceptUser = request.user
    acceptProject = Project.objects.get(pk=projectId)
    invitation = invitedDev.objects.filter(Q(user=acceptUser) & Q(project=acceptProject))
    if invitation:
        acceptUser.project.add(acceptProject)
        acceptUser.devTeam = True
        acceptUser.save()
        invitation.first().delete()
        return render(request,'acceptDevTeam.html')

@login_required
def inviteScrumMaster(request):
    if request.user.is_developer:
        if request.user.is_productOwner == True:
            return render (request, 'inviteScrumMaster.html')

@login_required
def inviteScrumMasterOperation(request):
    if request.user.is_developer:
        if request.user.is_productOwner == True:
            scrumMaster = User.objects.filter(Q(project = request.user.project.all().first()) & Q(scrumMaster = True))
            if scrumMaster:
                target = scrumMaster.first()
                msg = f'{target.username} is monitoring this project! There can only be one scrum master.' 
                data = {'msg': msg, 'go': False}
                return JsonResponse(data,safe = False)
            else:
                email = request.POST.get('address','')
                user = User.objects.filter(email= email)
                if user:
                    invitation = invitedScrumMaster.objects.filter(Q(user=user.first()) & Q(project=request.user.project.all().first()))
                    project = user.first().project.all()
                    if user.first().is_manager == False:
                        data = {'msg': 'The user is not a manager, hence cannot be added as scrum master', 'go': False}
                        return JsonResponse(data,safe = False)
                    elif invitation:
                        data = {'msg': 'The user is already invited to this project', 'go': False}
                        return JsonResponse(data,safe = False)
                    else: 
                        data = {'msg': 'can add', 'go': True}
                        addUser = user.first()
                        addProject = request.user.project.all().first()
                        addInvitation = invitedScrumMaster(user=addUser, project = addProject)
                        addInvitation.save()
                        title = f'backTrack Invitation from the project {addProject.title}'
                        content = f'Please click the link below to join the project: localhost:8000/myApp/acceptScrumMaster/{addProject.pk}'
                        host = 'hku.backtrack@gmail.com'
                        recipients = [addUser.email,]
                        send_mail(title,
                            content,
                            host,
                            recipients,
                            fail_silently=False)
                        return JsonResponse(data,safe = False)

@login_required
def acceptScrumMaster(request,projectId):
    acceptUser = request.user
    acceptProject = Project.objects.get(pk=projectId)
    invitation = invitedScrumMaster.objects.filter(Q(user=acceptUser) & Q(project=acceptProject))
    if invitation:
        acceptUser.project.add(acceptProject)
        acceptUser.scrumMaster = True
        acceptUser.save()
        invitation.first().delete()
        return render(request,'acceptScrumMaster.html')

@login_required
def productBacklogRoute(request):
    if request.user.is_developer:
        if request.user.is_productOwner:
            return ProductOwnerViewCurrent.as_view(projectId=request.user.project.all().first().pk)(request)
        elif request.user.is_devTeam:
                return NonProductOwnerViewCurrent.as_view(projectId=request.user.project.all().first().pk)(request)
        else:
            return DevLoginNoProject.as_view()(request)
    elif request.user.is_manager:
        return ScrumMasterPbList.as_view()(request)

@login_required
def scrumMasterProductBacklogRoute(request, projectId = None):
    if request.user.is_manager:
        if request.user.is_scrumMaster:
            target = Project.objects.get(pk=projectId)
            flag = False
            for project in request.user.project.all():
                if project == target:
                    flag = True
                    break
            if flag:
                return NonProductOwnerViewCurrent.as_view(projectId=projectId)(request)



@login_required
def scrumMasterSprintBacklogRoute(request, projectId = None):
    if request.user.is_manager:
        if request.user.is_scrumMaster:
            target = Project.objects.get(pk=projectId)
            flag = False
            for project in request.user.project.all():
                if project == target:
                    flag = True
                    break
            if flag:
                return SprintBacklogNonDev.as_view(projectId=projectId)(request)

@login_required
def sprintBacklogRoute(request):
    if request.user.is_developer:
        if request.user.is_productOwner:
            return SprintBacklogNonDev.as_view(projectId=request.user.project.all().first().pk)(request)
        elif request.user.is_devTeam:
                return SprintBacklog.as_view(projectId=request.user.project.all().first().pk)(request)
        else:
            return DevLoginNoProject.as_view()(request)
    elif request.user.is_manager:
        return scrumMasterSprintBacklogs.as_view()(request)

@login_required
def scrumMasterProductBacklogAllRoute(request, projectId = None):
    if request.user.is_manager:
        if request.user.is_scrumMaster:
            target = Project.objects.get(pk=projectId)
            flag = False
            for project in request.user.project.all():
                if project == target:
                    flag = True
                    break
            if flag:
                return NonProductOwnerViewAll.as_view(projectId=projectId)(request)

@login_required
def productBacklogAllRoute(request):
    if request.user.is_developer:
        if request.user.is_productOwner:
            return ProductOwnerViewAll.as_view(projectId=request.user.project.all().first().pk)(request)
        elif request.user.is_devTeam:
                return NonProductOwnerViewAll.as_view(projectId=request.user.project.all().first().pk)(request)
        else:
            return DevLoginNoProject.as_view()(request)
    elif request.user.is_manager:
        return ScrumMasterPbList.as_view()(request)

class ProductOwnerViewCurrent(TemplateView):
    template_name = 'PBI_list.html'
    projectId = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        pbis = PBI.objects.order_by('priority').filter(project__pk=self.projectId).all()
            
        context['pbi_list'] = pbis

        return context

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

    def priority_insert_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        targetPriority = request.POST.get('targetPriority', '')
        obj = PBI.objects.filter(id=myid).first()
        target = PBI.objects.filter(Q(priority=targetPriority) & Q(project=request.user.project.all().first()) ).first()
        print(target.name)
        if target.status == 1 or target.status == 4:
            targetPriority = target.priority
            if target.status == 1 and targetPriority != obj.priority:
                if targetPriority < obj.priority:
                    affecteds = PBI.objects.order_by('-priority').filter(Q(project = obj.project) & Q(priority__lt = obj.priority) & Q(priority__gte = target.priority))
                    obj.priority = None
                    obj.save()
                    for affected in affecteds:
                        affected.priority = affected.priority + 1
                        affected.save()
                else:
                    affecteds = PBI.objects.order_by('priority').filter(Q(project = obj.project) & Q(priority__gt = obj.priority) & Q(priority__lte = target.priority))
                    obj.priority = None
                    obj.save()
                    for affected in affecteds:
                        affected.priority = affected.priority - 1
                        affected.save()
                obj.priority = targetPriority
                obj.save()
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def status_change_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        newStatus = request.POST.get('newStatus', '')
        obj = PBI.objects.filter(id=myid).first()
        obj.status =  newStatus
        if newStatus == "1":
            obj.sprintNo = None
        obj.save()
        # return HttpResponseRedirect('/myApp/pbis')
        # return render(request, 'PBI_list.html', {})
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def pbi_delete_view(request):
        myid = request.POST.get('myid', '') # function to get param from POST
        obj = PBI.objects.filter(id=myid).first()
        mypriority = obj.priority
        obj.delete()
        others = PBI.objects.order_by('priority').filter(project=obj.project)
        for other in others:
            if (other.priority and other.priority > mypriority):
                other.priority = (other.priority - 1)
                other.save()
        context = {
        }
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

    # def priority_auto_view(request):
    #     myid = request.POST.get('myid', '') # function to get param from POST
    #     obj = PBI.objects.filter(id=myid).first()
    #     # for obj in objs:
    #     obj.priority = obj.priority - 1
    #     obj.save()
    #     # return HttpResponseRedirect('/myApp/pbis')
    #     # return render(request, 'PBI_list.html', {})
    #     return HttpResponseRedirect(reverse_lazy('pbi_list'))

    def process_done_view(request):
        myid = request.POST.get('myid', '')
        obj = PBI.objects.filter(id=myid).first()
        mypriority = obj.priority
        obj.priority = None
        obj.status = 3
        obj.save()
        others = PBI.objects.order_by('priority').filter(project=obj.project)
        for other in others:
            if other.priority != None and mypriority != None:
                if other.priority > mypriority:
                    other.priority = (other.priority - 1)
                    other.save()
        return HttpResponseRedirect(reverse_lazy('pbi_list'))

class NonProductOwnerViewCurrent(TemplateView):
    template_name = 'PBI_list_nonPM.html'
    projectId = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        project = self.projectId
        projectName = Project.objects.get(pk=self.projectId).title;
        pbis = PBI.objects.order_by('priority').filter(project__pk=self.projectId).all()
        
        context['pbi_list'] = pbis
        context['project'] = project
        context['projectName'] = projectName
        return context


class DevLoginNoProject(TemplateView):
    template_name = 'dev_noProject.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context

class ScrumMasterPbList(TemplateView):
    template_name = 'scrumMasterPbList.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context

class scrumMasterSprintBacklogs(TemplateView):
    template_name = 'scrumMasterSbList.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductOwnerViewAll(TemplateView):
    template_name = 'PBI_fullList.html'
    projectId = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        pbis = PBI.objects.order_by('sprintNo').filter(project__pk=self.projectId).all()
            
        context['pbi_list'] = pbis

        return context

class NonProductOwnerViewAll(TemplateView):
    template_name = 'PBI_fullList_nonPM.html'
    projectId = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        project = self.projectId
        projectName = Project.objects.get(pk=self.projectId).title;
        pbis = PBI.objects.order_by('sprintNo').filter(project__pk=self.projectId).all()
            
        context['pbi_list'] = pbis
        context['project'] = project
        context['projectName'] = projectName

        return context

class PbiCreation(TemplateView):
    template_name = "pbiCreation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def create(request):
        projectId = request.POST.get('project', '')
        project = Project.objects.get(pk=projectId)
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        estimate = request.POST.get('estimate', '')
        addedPBI = PBI(name = name, Description = description, estimate = estimate, project = project, status = 1)
        addedPBI.save()
        return HttpResponseRedirect(reverse_lazy('pbi_list'))


# class PBICreateView(BSModalCreateView):
#     model = PBI
#     template_name = 'modalPage/PBI_create.html'
#     form_class = PBIForm
#     success_message = 'Success: PBI was created.'
#     success_url = reverse_lazy('all_pbis')

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

# class PBIDeleteView(BSModalDeleteView):
#     model = PBI
#     template_name = 'modalPage/PBI_delete.html'
#     success_message = 'Success: PBI was deleted.'
#     success_url = reverse_lazy('pbi_list')

## Views for sprint backlog functions
class SprintBacklog(TemplateView):
    template_name = "sprintBacklog.html"
    projectId = None

    def get_context_data(self, **kwargs):
        # owner = self.kwargs['Users']

        context = super().get_context_data(**kwargs)

        #temp project value before the authentication is inplaced.
        project = Project.objects.get(pk=self.projectId)
        pbis = PickedPBI.objects.order_by('pbi__priority').filter(pbi__project=project)
        tasks = Task.objects.filter(pbiPicked__pbi__project=project)
        pbisToBePulled = PBI.objects.order_by('priority').filter(Q(project = project) & Q(status = 1))
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
        context['pbis'] = pbis
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
        obj.sprintNo = obj.project.sprint
        obj.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def deletePulled(request):
        pbiid = request.POST.get('pbiid', '')
        obj = PickedPBI.objects.filter(id=pbiid).first()
        flag = False
        relatedDoneTasks = Task.objects.filter(Q(pbiPicked=obj) & Q(status = 3))
        if relatedDoneTasks:
            flag = True
        pbi = obj.pbi
        obj.delete()
        if flag:
            pbi.status = 4
        else:
            pbi.status = 1
            pbi.sprintNo = None
        pbi.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def clear(request):
        project = request.user.project.all().first()
        pbis = []
        pickedPbis = PickedPBI.objects.order_by('pbi__priority').filter(pbi__project = project)
        others = PBI.objects.order_by('priority').filter(project=project)
        for pbi in pickedPbis:
            if pbi.pbi.project == project:
                pbis.append(pbi.pbi)
                pbi.delete()
        for pbi in pbis:
            pbi.refresh_from_db()
            pbi.status = 3
            mypriority = pbi.priority
            pbi.priority = None
            pbi.save()
            for other in others:
                other.refresh_from_db()
                if other.priority != None and mypriority != None:
                    if other.priority > mypriority:
                        other.priority = (other.priority - 1)
                        other.save()
        project.sprint = project.sprint + 1
        project.sprintEffort = 0
        project.started = False
        project.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

    def startProject(request):
        project = request.user.project.all().first()
        project.started = True
        project.save()
        return HttpResponseRedirect(reverse_lazy('sprint_backlog'))

## Views for sprint backlog functions
class SprintBacklogNonDev(TemplateView):
    template_name = "sprintBacklog_nonDev.html"
    projectId = None

    def get_context_data(self, **kwargs):
        # owner = self.kwargs['Users']

        context = super().get_context_data(**kwargs)

        #temp project value before the authentication is inplaced.
        project = Project.objects.get(pk=self.projectId)
        pbis = PickedPBI.objects.order_by('pbi__priority').filter(pbi__project=project)
        tasks = Task.objects.filter(pbiPicked__pbi__project=project)
        pbisToBePulled = PBI.objects.order_by('priority').filter(Q(project = project) & Q(status = 1))
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
        context['pbis'] = pbis
        context['notStartedTasks'] = notStarted
        context['inProgressTasks'] = inProgress
        context['doneTasks'] = done
        context['pullItems'] = pullItems
        context['taskNum'] = taskNum
        return context

class SprintUpdateView(BSModalUpdateView):
    model = Project
    template_name = 'modalPage/sprintUpdate.html'
    form_class = SprintUpdateForm
    success_message = 'Success: PBI was updated.'
    success_url = reverse_lazy('sprint_backlog')


class taskDetails(TemplateView):
    template_name = "taskDetails.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_devTeam == False:
            self.template_name = "taskDetails_nonDev.html"
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
        if request.user.project.all().first().started == True:
            taskid = request.POST.get('taskid', '')
            task = Task.objects.get(pk=taskid)
            dev = request.user
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
        project = self.request.user.project.all().first()
        context = super().get_context_data(**kwargs)
        pickedPbi = PickedPBI.objects.filter(pbi__project = project)
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
