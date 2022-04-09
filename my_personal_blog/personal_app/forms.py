from dataclasses import fields
from tkinter import Widget
from django import forms
from personal_app.models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
    
        # inside the Meta class we should put the widgets. We can use those widgets for styling in CSS.
        widgets = {
            "title":forms.TextInput(attrs={"class":"textinputclass"}),
            "body":forms.Textarea(attrs={"class":"editable medium-editor-textarea postcontent"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "text"]

        # "textinputclass" is our class. But "editable medium-editor-textarea" is a standard bootstrap class.
        widgets = {
            "text":forms.Textarea(attrs={"class":"editable medium-editor-textarea"})
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) # not necessary since "password" field is already built-in.

    class Meta():
        model = User
        fields = ["username", "email", "password"]
