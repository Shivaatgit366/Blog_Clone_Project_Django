from personal_app import views
from django.urls import path
from personal_app.views import (AboutView, PostListView, DraftListView,
                                PostDetailView, PostCreateView, PostUpdateView, PostDeleteView)


app_name = "personal_app"


urlpatterns = [
    path("create_post/", PostCreateView.as_view(), name="post_create"),
    path("register/", views.register, name="register"),
    path("", PostListView.as_view(), name="post_list"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/<pk>/", PostDetailView.as_view(), name="post_detail"),
    path("update_post/<pk>/", PostUpdateView.as_view(), name="post_update"),
    path("delete_post/<pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("post_drafts/", DraftListView.as_view(), name="draft_list"),
    path("comment/post/<pk>/", views.add_comment_to_post, name="add_comment"),
    path("comment/<pk>/approved/", views.approve_comment, name="approve_comment"),
    path("comment/<pk>/removed/", views.comment_remove, name="remove_comment"),
    path("publish_post/<pk>/", views.post_publish, name="publish_post")
]
