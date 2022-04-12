from django.core.exceptions import ValidationError
from typing import Literal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, TemplateView, ListView, CreateView,
                                  DetailView, UpdateView, DeleteView)

from django.template.loader import get_template

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from personal_app.forms import PostForm, CommentForm, UserForm
from personal_app.models import Post, Comment
from typing import Dict, List, Any


# Create your views here.

# Notes:-
# "Post.objects" --> it is a query.
# "Post.objects.all()" --> it means "select * from Post;" in Mysql database.
# "Post.objects.first()" --> it means select only one row, limit=1 in Mysql database.
# "filter" word is used for filtering the records in the database. In Mysql, we use "WHERE" clause.
# "modelname.fieldnames.all()" --> means to select all the records from those columns present in that table.


class AboutView(TemplateView):
    template_name = "personal_app/about.html"


class PostListView(ListView):  # we are dealing with the CRUD part of the database
    model = Post
    template_name = "personal_app/post_list.html"
    context_object_name = "list_of_post_objects"

    # Remember this below function returns a "class"/dictionary which is inherited from its ancestors.
    # this function is already built in by django and it is coming from the ancestor classes.
    # if we want to change any property, then we can use it.
    def get_queryset(self):
        dict = super().get_queryset()
        # "order_by" usually sorts the data in the ascending order, that means oldest "blog" will come first.
        # so, we should simply put "-" sign so that db sorts the records in the descending order and we get latest "blog" in the first record.
        # "__" used for custom lookups. These lookups are used to put the constraints on a field/column. "lte" means less than or equal to.
        
        # select all the records where the records should be created in the present moment or the past.
        if not self.request.user.is_authenticated:
            objects_list = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
        else:
            objects_list = Post.objects.filter(
                published_date__lte=timezone.now(),
                author=self.request.user
            ).order_by("-published_date")     
        return objects_list


class PostDetailView(DetailView):
    model = Post
    template_name = "personal_app/post_detail.html"

    # "context_object_name" is the "key" in the context dictionary. This key will be used in template tag.
    context_object_name = "post_object"


class PostCreateView(LoginRequiredMixin, CreateView):
    # this "CreateView" cbv creates a model-form. We should specify the model name and fields to be displayed.
    # if we have already created a form/model-form, then we should just mention it as "form_class".

    # decorators are used for the function based views. In CBVs, we use "mixins". Read the documentation.
    login_url = "/user/login/"
    redirect_field_name = "personal_app/post_detail.html"
    model = Post

    # if we are using the form, then mention the "form_class" as shown below.
    form_class = PostForm

    # an object called "form" is created by django itself using "form_class/model form".
    # It has "author" field, that author should be same as the "request sending author".
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    login_url = "/user/login/"

    # django automatically creates an object called "form", we should just create the template with the name "model_update_form".
    template_name_suffix = "_update_form"

    # Remember that we can not give the below success_url method for redirect response because "post_detail" takes primary key parameter.
    # We can not give primary key if we use below function. So we should create a custom function to redirect the page.
    
    # success_url = reverse_lazy('personal_app:post_detail') ---------> Do not use this.

    # create a function to redirect the page.
    def redirector(self):
        saved_pk = self.pk
        return reverse("personal_app:post_detail", pk=saved_pk)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('personal_app:post_list')


# we want to see all the objects including those objects which are not published yet. So, published date will be "null" for the unpublished posts/blogs.
class DraftListView(LoginRequiredMixin, ListView):
    # we are using the same "query_set" as we used for "PostListView".
    # "query_set" is a built in function/property from the ancestor class. It is already present in the present class.
    # even though a class is inherited from the ancestors, we can change the current properties of the class.

    # we should create a new html file called "post_draft_list.html" to view the list of drafts.
    login_url = "/user/login/"
    model = Post
    template_name = "personal_app/post_draft_list.html"
    context_object_name = "list_of_draft_objects"

    # we can use the in-built function to modify the properties. QuerySet function gives the "cursor" as the output.
    # Cursor means a "list of objects". By putting "filter" function we get the list of objects.
    # After getting the list of objects, put a where/filter clause.
    # Select only those post objects which have the "author name" equal to the "requesting user".
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True,
        author = self.request.user).order_by("-created_date")


#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################


# from here on, we will use function based views.


# post should be published, we should write a function for that.
@login_required
def post_publish(request, pk):
    post_object = get_object_or_404(Post, pk=pk)
    post_object.publish()
    # use "reverse" function only for the class based views. It won't work for normal functions.
    return redirect("personal_app:post_detail", pk=post_object.pk)


# user can comment on any blog without registration also.
def add_comment_to_post(request, pk):
    post_object = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form_object = CommentForm(request.POST)
        if form_object.is_valid():
            comment_object = form_object.save(commit=False)
            # the above object should be present in the "post" column of Comment table. So, we should confirm it.
            # then the comment will be saved in the Comment table. Then response will be redirected to another page.
            comment_object.post = post_object
            comment_object.save()
            # "reverse" function works only for the class based views.
            return redirect("personal_app:post_detail", pk=post_object.pk)

    else:
        form_object = CommentForm()
    return render(request, "personal_app/comment_form.html", {"form_key": form_object})


# comment should be approved inorder to get displayed.
# whenever a person comments on a blog, it will be saved in the Comment table. 
# by default, every comment is not approved.
@login_required
def approve_comment(request, pk):
    comment_object = get_object_or_404(Comment, pk=pk)
    # "approve" method is defined in the Comment class. When we call this function, we get "approved_comment=True".
    if comment_object.post.author == request.user:
        comment_object.approve()
    return redirect("personal_app:post_detail", pk=comment_object.post.pk)


@login_required
def comment_remove(request, pk):
    comment_object = get_object_or_404(Comment, pk=pk)
    # before deleting the object, save the primary key in a variable.
    pk_saved = comment_object.post.pk
    if comment_object.post.author == request.user:
        comment_object.delete()
    return redirect("personal_app:post_detail", pk=pk_saved)


def register(request):
    if request.method == "POST":
        user_form_object = UserForm(request.POST)

        if user_form_object.is_valid():
            user_db_obj = user_form_object.save(commit=False)
            user_db_obj.set_password(user_db_obj.password)  # Hashing the plain password in the database.
            user_db_obj.save()  # by default, save() method keeps "commit=True"

            # for "post" request, render the view with below dictionary
            display_dict = {"user_form": user_db_obj, "registered": True}

        else:
            raise ValidationError("form is not valid")

    # for "get" request below code will be executed
    else:
        empty_user_object = UserForm()

        # for "get" request, render the view with below dictionary
        display_dict = {"user_form": empty_user_object, "registered": False}

    # for any kind of requests, just render the below code
    return render(request,"personal_app/register.html",context=display_dict)
