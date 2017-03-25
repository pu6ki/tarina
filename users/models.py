from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.URLField(
        default='http://tarina.herokuapp.com/static/images/default.jpg',
        blank=False
    )

    def __str__(self):
        return self.user.username
