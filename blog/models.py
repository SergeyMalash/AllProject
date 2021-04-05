from django.db import models
from django.urls import reverse
from accounts.models import Account
from slugify import slugify


class Article(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=5000)
    liked_users = models.ManyToManyField(Account, related_name='liked_articles', blank=True)
    disliked_users = models.ManyToManyField(Account, related_name='disliked_articles', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + f'-{self.pk}'
            self.save(update_fields=['slug'])

    def rating(self):
        return self.liked_users.all().count() + self.disliked_users.all().count()

    def get_absolute_url(self):
        return reverse('article', args=[self.slug])
