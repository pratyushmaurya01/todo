from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustumLoginView,RegisterPage,TaskDone
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustumLoginView.as_view(), name="login"),
    path('register/',RegisterPage.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name='task-delete'),
     path('task-done/<int:pk>/', TaskDone.as_view(), name='task-done'), 

]