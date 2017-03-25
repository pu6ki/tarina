from django.db import models

from users.models import Author


class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']
        verbose_name_plural = 'stories'

    def __str__(self):
        return '{} by {} ({})'.format(self.title, self.author, self.posted_on)
