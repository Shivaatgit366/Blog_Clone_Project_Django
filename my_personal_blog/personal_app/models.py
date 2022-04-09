from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    # when we give foreign key, remember that the Model name should not be "a string" in the django latest version.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # let us keep a button, when the button is hit for "publish", the below function gets executed.
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # the below function will return only the approved comments as a list.
    # This function gives "a list of all approved comments" for a particular "post/blog".
    # When we put "filter" function, then it returns the list of all the items.
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # we need a "thank you" page or we can use "get_absolute_url" method to redirect the response to any other page.
    def get_absolute_url(self):
    # return reverse("url path should be provided in template tag")
        return reverse("personal_app:post_detail",kwargs={"pk":self.pk})

    # make a data representation/string representation of the class/object using special function.
    def __str__(self):
        return self.title


class Comment(models.Model):
    # there are three ways to write foreign key in django.
    # first two methods needs the models to be in the same file. [Parent model first, child model next] or [child model first, parent model next] these two combinations are used.
    # the third method is shown in the below example. We can keep the models in any of the apps.
    # when we use several apps, we need to mention the name of the app. Django will find the model in that app.

    # when we make "post" column, it will be automatically renamed to "post_id" name by django. The IDs will be mapped automatically by django.
    # "related_name" tells django to create a column with [related_name]_id in the above table. The IDs will be mapped automatically by django.
    
    # Database shows only the "post_id" as given in the above description. But for ORM, django provides the full "post" object in this column.
    # The column "post" in Comment table will have the "post objects" created by the django for the ORM.
    # Similarly, the column "comments" in Post table will have the "comment objects" created by the django for the ORM.
    # Note:- Database shows only the IDs as described above. But django provides the full object for the ORM purpose.
    
    # when we mention the model name in foreign key, we should not make it "a string" in the latest django versions.
    post = models.ForeignKey(Post, related_name= "comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # we keep a button for the approval, whenever the button is hit, this below function will be called. So, "approved_comment" will become "True".
    def approve(self):
        self.approved_comment = True
        self.save()

    # writing the function "get_absolute_url" to redirect the response to other page.
    def get_absolute_url(self):
        return reverse("personal_app:post_list")

    # string representation of the object. Text content of the comment will be shown here.
    def __str__(self):
        return self.text
