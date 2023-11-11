from urllib.request import Request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView
from .forms import RegisterUserForm, ChangeStatusRequest
from .models import Application, Category
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View




# Create your views here.
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')


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


class ApplicationsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'profil.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


class ApplicationDelete(ApplicationListView):
    model = Application
    context_object_name = 'application'
    template_name = 'delete.html'
    success_url = reverse_lazy('request')


class MyPostListViews(generic.ListView):
    model = Application
    context_object_name = 'application'
    template_name = 'order.html'

    def get_queryset(self):
        return Application.object.filter(user=self.request.user).object_by('-date')


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['title', 'category', 'photo_file']
    template_name = 'order.html'
    success_url = reverse_lazy('request')


def request_catalog(request):
    return render(request, "order.html")


def add_request(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        request.objects.create(title=title, description=description)
        return redirect('list_requests')
    return render(request, 'order.html')







class ApplicationListViewAdmin(generic.ListView):
    model = Application
    template_name = 'base.html'
    context_object_name = 'application_list'
    def get_queryset(self):
        return Application.objects.order_by('-date')[:4]

class ApplicationListView(generic.ListView):
    model = Application
    paginate_by = 4
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_application'] = Application.objects.filter(status__exact='Принято в работу').count()
        return context


class CategoryView(generic.ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

class CategoryDelete(DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category')

class CategoryCreate(CreateView):
    model = Category
    fields = ['name']
    template_name = 'create_category.html'
    success_url = reverse_lazy('category')

class ChangeStatusRequest(UpdateView):
    model = Application
    form_class = ChangeStatusRequest
    template_name = 'change_status.html'
    success_url = reverse_lazy('superadmin')


