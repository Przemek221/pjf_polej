from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Something
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterUserForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# from django.contrib.auth.forms import UserCreationForm

class AllToDos(ListView):
    model = Something
    template_name = "sampleApp/index.html"


# argument dla fcji, dla strony index html
sth = [
    {'number': 5, 'desc': 'sss'},
    {'number': 1, 'desc': 'ddd'}
]


def xxx(request):
    arg = {
        'title': 'abc',
        'object_list': sth
    }
    return render(request, 'sampleApp/index.html', arg)


def displayPosts(request):
    arg = {
        'title': 'abc',
        'posts': Post.objects.all()
    }
    return render(request, 'sampleApp/home.html', arg)


class DisplayPosts(ListView):
    model = Post
    # by default template name is: appName/modelName_viewType
    template_name = 'sampleApp/home.html'
    context_object_name = 'posts'
    ordering = ['-createdDate']
    paginate_by = 10


class DisplayUsersPosts(ListView):
    model = Post
    # by default template name is: appName/modelName_viewType
    template_name = 'sampleApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(creator=user).order_by('-createdDate')


class PostDetails(DetailView):
    model = Post


# to implement post details with comments section,
# it will be easier to use the function based view

def postDetails(request, post_id):
    arg = {
        'object': Post.objects.get(id=post_id)
    }
    return render(request, 'sampleApp/post_detail.html', arg)


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        # assigning creator before validation
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        # assigning creator before validation
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/../home'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.creator


# def przyklkad(request):
#     argument = {'klucz': "wartosc"}
#     # return render(request, 'sampleApp/register.html', argument)
#     return render(request, 'sampleApp/register.html', {'argument': 'wartosc'})


def registerUser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"User {username} registered")
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'sampleApp/register.html', {'form': form, 'title': 'register'})


@login_required
def profile(request):
    if request.method == 'POST':
        update_user_form = UpdateUserForm(request.POST, instance=request.user)
        update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if update_profile_form.is_valid() and update_user_form.is_valid():
            update_user_form.save()
            update_profile_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')

    else:
        update_user_form = UpdateUserForm(instance=request.user)
        update_profile_form = UpdateProfileForm(instance=request.user.userprofile)

    arg = {
        'update_user_form': update_user_form,
        'update_profile_form': update_profile_form
    }
    return render(request, 'sampleApp/profile.html', arg)
