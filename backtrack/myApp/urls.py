from django.urls import path
from myApp import views

urlpatterns = [
	# project level views
	path('loginRoute', views.loginRoute,name = 'loginRoute'),
	path('createProject', views.projectCreation,name = 'project_creation'),
	path('createProjectOperation', views.projectCreationOperation,name = 'project_creation_operation'),
	# view for showing all pbis
	path('pbis/', views.productBacklogRoute, name='pbi_list'),
	path('allPbis/', views.productBacklogAllRoute, name='all_pbis'),
	path('pbis/<int:projectId>', views.scrumMasterProductBacklogRoute, name='pbi_list_scrum'),
	path('allPbis/<int:projectId>', views.scrumMasterProductBacklogAllRoute, name='all_pbis_scrum'),
	path('pbis/detail/<int:pk>', views.PBIDetailView.as_view(), name='pbi_detail'),
	path('pbis/realDetail/<int:pk>', views.PBIRealDetailView.as_view(), name='pbi_realDetail'),
	path('pbis/create', views.PbiCreation.as_view(), name='pbi_create'),
	path('pbis/create/create', views.PbiCreation.create, name='pbi_create_operation'),
	path('pbis/up', views.ProductOwnerViewCurrent.priority_up_view, name='pbi_up'),
	path('pbis/down', views.ProductOwnerViewCurrent.priority_down_view, name='pbi_down'),
	path('pbis/statusChange', views.ProductOwnerViewCurrent.status_change_view, name='status_change'),
	path('pbis/priorityInsert', views.ProductOwnerViewCurrent.priority_insert_view, name='priority_insert'),
	path('pbis/delete', views.ProductOwnerViewCurrent.pbi_delete_view, name='pbi_delete'),
	path('pbis/priorityAutoUpdate', views.ProductOwnerViewCurrent.priority_auto_view, name='priority_auto'),
	path('pbis/processDone', views.ProductOwnerViewCurrent.process_done_view, name='process_done'),
	# paths related to sprint backlog
	path('sprintBacklog/', views.sprintBacklogRoute, name='sprint_backlog'),
	path('sprintBacklog/<int:projectId>', views.scrumMasterSprintBacklogRoute, name='sprint_backlog_scrum'),
	path('taskDetails/<int:task>',views.taskDetails.as_view(),name='task_details'),
	path('taskDetails/edit',views.taskDetails.edit,name='task_details_edit'),
	path('taskDetails/pick',views.taskDetails.pick,name='task_details_pick'),
	path('taskDetails/changeStatus',views.taskDetails.changeStatus,name='task_details_changeStatus'),
	path('taskDetails/changeComplete',views.taskDetails.changeComplete,name='task_details_changeComplete'),
	path('taskDetails/delete',views.taskDetails.delete,name='task_details_delete'),
	path('sprintBacklog/pull', views.SprintBacklog.pull_task_view, name='task_pull'),
	path('sprintBacklog/taskCreation', views.taskCreation.as_view(), name='task_creation'),
	path('sprintBacklog/taskCreation/create', views.taskCreation.create, name='task_creation_create'),	
	path('sprintBacklog/deletePulled', views.SprintBacklog.deletePulled, name='task_delete'),	
	path('sprintBacklog/clear', views.SprintBacklog.clear, name='sprintBacklog_clear'),
	path('sprintBacklog/startProject', views.SprintBacklog.startProject, name='sprintBacklog_startProject'),
	path('sprintBacklog/changeSprintInfo/<int:pk>', views.SprintUpdateView.as_view(), name='sprintBacklog_changeSprintInfo'),
]
