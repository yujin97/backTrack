from django.urls import path
from myApp import views

urlpatterns = [
	# prefered view for specific pbi details
	# path('customerOrders/<int:customer>',views.CustomerViewOrders.as_view(),name='customer-orders'),
	# view for showing all pbis
	path('pbis/', views.ProductOwnerViewCurrent.as_view(), name='pbi_list'),
	path('allPbis/', views.ProductOwnerViewAll.as_view(), name='all_pbis'),
	path('pbis/detail/<int:pk>', views.PBIDetailView.as_view(), name='pbi_detail'),
	path('pbis/realDetail/<int:pk>', views.PBIRealDetailView.as_view(), name='pbi_realDetail'),
	path('pbis/delete/<int:pk>', views.PBIDeleteView.as_view(), name='pbi_delete'),
	path('pbis/create', views.PBICreateView.as_view(), name='pbi_create'),
	path('pbis/up', views.ProductOwnerViewCurrent.priority_up_view, name='pbi_up'),
	path('pbis/down', views.ProductOwnerViewCurrent.priority_down_view, name='pbi_down'),
	path('pbis/statusChange', views.ProductOwnerViewCurrent.status_change_view, name='status_change'),
	path('pbis/priorityInsert', views.ProductOwnerViewCurrent.priority_insert_view, name='priority_insert'),
	path('pbis/delete', views.ProductOwnerViewCurrent.pbi_delete_view, name='pbi_delete'),
	path('pbis/priorityAutoUpdate', views.ProductOwnerViewCurrent.priority_auto_view, name='priority_auto'),
	path('pbis/processDone', views.ProductOwnerViewCurrent.process_done_view, name='process_done'),
	# paths related to sprint backlog
	path('sprintBacklog/', views.SprintBacklog.as_view(), name='sprint_backlog'),
	path('taskDetails/<int:task>',views.taskDetails.as_view(),name='task_details'),
	path('taskDetails/edit',views.taskDetails.edit,name='task_details_edit'),
	path('taskDetails/pick',views.taskDetails.pick,name='task_details_pick'),
	path('taskDetails/changeStatus',views.taskDetails.changeStatus,name='task_details_changeStatus'),
	path('taskDetails/changeComplete',views.taskDetails.changeComplete,name='task_details_changeComplete'),
	path('taskDetails/delete',views.taskDetails.delete,name='task_details_delete'),
	path('sprintBacklog/pull', views.SprintBacklog.pull_task_view, name='task_pull'),
	path('sprintBacklog/taskCreation', views.taskCreation.as_view(), name='task_creation'),
	path('sprintBacklog/taskCreation/create', views.taskCreation.create, name='task_creation_create'),	
	path('sprintBacklog/deletePulled', views.SprintBacklog.deletePulled, name='task_creation_create'),	
	path('sprintBacklog/clear', views.SprintBacklog.clear, name='sprintBacklog_clear'),
	path('sprintBacklog/startProject', views.SprintBacklog.startProject, name='sprintBacklog_startProject'),
	path('sprintBacklog/changeSprintInfo/<int:pk>', views.SprintUpdateView.as_view(), name='sprintBacklog_changeSprintInfo'),
]
