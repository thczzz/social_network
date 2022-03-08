from django.contrib import admin
from post import models

admin.site.register(models.Post)
admin.site.register(models.PostLike)
admin.site.register(models.PostComment)
