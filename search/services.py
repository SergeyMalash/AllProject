from django.db.models import Q

from accounts.models import Account
from blog.models import Article
from shortener.models import Tag, Url


def search_accounts(self):
    result = Account.objects.filter(username__icontains=self.search_text).exclude(username=self.request.user.username)
    return result


def search_tags(self):
    result = Tag.objects.filter(
        Q(title__icontains=self.search_text),
        Q(user=self.request.user)
    )
    return result


def search_urls(self):
    result = Url.objects.filter(
        Q(slug__icontains=self.search_text),
        Q(user=self.request.user)
    )
    return result


def search_articles(self):
    result = Article.objects.filter(title__icontains=self.search_text)
    return result
