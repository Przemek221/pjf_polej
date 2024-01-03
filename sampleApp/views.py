from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import (RegisterUserForm, UpdateUserForm, UpdateProfileForm,
                    CreatePostForm, CreatePostAttachmentForm)
from .models import Something, Post, Comment, PostAttachment


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


def display_posts(request):
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

    # def post_is_liked(self, post_id):
    #     likes_connected = get_object_or_404(Post, id=post_id)
    #     liked = False
    #     if likes_connected.likes.filter(id=self.request.user.id).exists():
    #         liked = True
    #     return liked

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        # data['post_is_liked'] = {}
        # for item in Post.objects.all():
        # for item in data['object_list']:
        #     data['post_is_liked'].update({f"{item.id}": self.post_is_liked(item.id)})
        # data['post_is_liked'].append(self.post_is_liked(item.id))

        return data


class DisplayUsersPosts(ListView):
    model = Post
    # by default template name is: appName/modelName_viewType
    template_name = 'sampleApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(creator=user).order_by('-createdDate')


@login_required
def post_like(request, pk):
    # post_id is taken from the form (it's a button value)
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))

    # int this case it's the post id, so it can be replaced with function argument, which is primary key
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    if request.POST.get('next') is not None:
        return HttpResponseRedirect(request.POST.get('next'))
    else:
        return redirect('home')
    # return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
    # return HttpResponseRedirect(reverse(request.POST.get('next'), args=[str(pk)]))


class PostDetails(DetailView):
    model = Post


def post_details(request, pk):
    arg = {
        'object': Post.objects.get(id=pk),
        'comments': Comment.objects.filter(relatedPost=pk),
        'attachments': PostAttachment.objects.filter(relatedPost=pk)
    }

    return render(request, 'sampleApp/post_detail.html', arg)


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    # https://stackoverflow.com/questions/35560758/django-createview-with-multiple-models
    def form_valid(self, form):
        # assigning creator before validation
        form.instance.creator = self.request.user

        return super().form_valid(form)


# zrobic clas based view z tworzeniem posta i dodawaniem od razu attachmentów jesli sa
def download_file(request, pk, attachment_id):
    file = PostAttachment.objects.filter(pk=attachment_id, relatedPost=pk).first()
    return FileResponse(file.attachment, as_attachment=True)


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST)
        post_attachment_form = CreatePostAttachmentForm(request.POST, request.FILES)
        uploaded_files = request.FILES.getlist('attachment')
        if post_form.is_valid() and post_attachment_form.is_valid():
            post_form.instance.creator = request.user
            created_post = post_form.save()

            for file in uploaded_files:
                temp = PostAttachment(attachment=file, relatedPost=created_post)
                temp.save()
                # post_attachment_form.instance.relatedPost = created_post
                # post_attachment_form.save()

            messages.success(request, "Post created")
            return redirect(reverse('post-detail', args=[created_post.id]))
    else:
        post_form = CreatePostForm()
        post_attachment_form = CreatePostAttachmentForm()

    arg = {
        'post_form': post_form,
        'post_attachment_form': post_attachment_form
    }
    return render(request, 'sampleApp/post_form_2.html', arg)


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    # def get_context_data(self, **kwargs):
    def get_post(self, **kwargs):
        # data = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return post
        # data['relatedPost'] = post
        # data['post_is_liked'] = {}
        # for item in Post.objects.all():
        # for item in data['object_list']:
        #     data['post_is_liked'].update({f"{item.id}": self.post_is_liked(item.id)})
        # data['post_is_liked'].append(self.post_is_liked(item.id))

    def form_valid(self, form):
        # assigning creator before validation
        form.instance.creator = self.request.user
        form.instance.relatedPost = self.get_post()
        return super().form_valid(form)


@login_required
def update_post(request, pk):
    old_post = get_object_or_404(Post, id=pk)
    # old_attachments = get_object_or_404(PostAttachment, relatedPost=old_post)
    old_attachments = PostAttachment.objects.filter(relatedPost=old_post)
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, instance=old_post)
        post_attachment_form = CreatePostAttachmentForm(request.POST, request.FILES, instance=old_attachments.first())
        uploaded_files = request.FILES.getlist('attachment')
        if post_form.is_valid() and post_attachment_form.is_valid():
            post_form.instance.creator = request.user
            created_post = post_form.save()

            for file in uploaded_files:
                temp = PostAttachment(attachment=file, relatedPost=created_post)

                temp.save()
                # post_attachment_form.instance.relatedPost = created_post
                # post_attachment_form.save()

            messages.success(request, "Post updated")
            return redirect(reverse('post-detail', args=[created_post.id]))
    else:
        post_form = CreatePostForm(instance=old_post)
        post_attachment_form = []
        for attachment in old_attachments:
            post_attachment_form.append(CreatePostAttachmentForm(instance=attachment))

    arg = {
        'post_form': post_form,
        'post_attachment_form': post_attachment_form
    }
    return render(request, 'sampleApp/post_form_2.html', arg)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']

        old_attachments = PostAttachment.objects.filter(relatedPost=pk)
        data['post_attachment_form'] = []
        if old_attachments.first() is not None:
            for attachment in old_attachments:
                data['post_attachment_form'].append(CreatePostAttachmentForm(instance=attachment))
        else:
            data['post_attachment_form'].append(CreatePostAttachmentForm())
        return data

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        created_post = get_object_or_404(Post, pk=pk)

        old_attachments = PostAttachment.objects.filter(relatedPost=pk)
        post_attachment_form = CreatePostAttachmentForm(request.POST, request.FILES, instance=old_attachments.first())
        uploaded_files = request.FILES.getlist('attachment')
        if post_attachment_form.is_valid():
            for file in uploaded_files:
                temp = PostAttachment(attachment=file, relatedPost=created_post)
                temp.save()

        return super().post(request)

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


# UserPassesTestMixin to dac tu u dolu w argumentach!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def comment_delete(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = pk
    comment.delete()

    return redirect(reverse('post-detail', args=[post_id]))


# def przyklkad(request):
#     argument = {'klucz': "wartosc"}
#     # return render(request, 'sampleApp/register.html', argument)
#     return render(request, 'sampleApp/register.html', {'argument': 'wartosc'})


def register_user(request):
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
