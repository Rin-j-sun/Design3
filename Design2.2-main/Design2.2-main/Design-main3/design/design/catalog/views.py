from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .forms import RegisterUserForm
from .models import Application, ChangeStatusRequest


# Create your views here.
def index(request):
    return render(request, 'index.html')


def profil(request):
    return render(request, 'profil.html')


def login(request):
    return render(request, 'registration/login.html')


def registration(request):
    return render(request, 'registration.html')


class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


class BBLogoutView(LogoutView):
    success_url = reverse_lazy('index')


class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'applications'

class ApplicationCreate(LoginRequiredMixin, CreateView): #создание заявки
    model = Application
    fields = ['title', 'category', 'photo_file']
    template_name = 'order.html'
    success_url = reverse_lazy('order')

    def request_category(request):
        return render(request, "order.html")

    def add_request(request):
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            request.objects.create(title=title, description=description)
            return redirect('list_order')
        return render(request, 'order.html')

class ApplicationDelete(ApplicationListView): #удаление заявки
    model = Application
    context_object_name = 'application'
    template_name = 'delete.html'
    success_url = reverse_lazy('order')


class ApplicationsByUserListView(LoginRequiredMixin, generic.ListView): #просмотр заявок
    model = Application
    template_name = 'profil.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

class MyPostListViews(generic.ListView): #создание заявки
    model = Application
    context_object_name = 'application'
    template_name = 'order.html'

class ChangeStatusRequest(UpdateView):
    model = Application
    form_class = ChangeStatusRequest
    template_name = 'status_change.html'
    success_url = reverse_lazy('profil')





