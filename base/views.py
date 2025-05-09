from django.shortcuts import HttpResponseRedirect,redirect
from django.views.generic.list  import ListView
from django.views.generic.detail  import DetailView
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustumLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(request, *args, **kwargs)
    

    


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        scearh_input = self.request.GET.get('scearch-area', '') 
        if scearh_input:
            context['tasks'] = context['tasks'].filter(title__icontains = scearh_input)
        context['scearch_input'] = scearh_input
        return context
         

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskDone(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_done.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.complete = True
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks'))

# class TaskReorder(View):
#     def post(self, request):
#         form = PositionForm(request.POST)

#         if form.is_valid():
#             positionList = form.cleaned_data["position"].split(',')

#             with transaction.atomic():
#                 self.request.user.set_task_order(positionList)

#         return redirect(reverse_lazy('tasks'))