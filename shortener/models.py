from io import BytesIO

from django.db import models
from django.urls import reverse
from django.core import validators

from accounts.models import Account
from shortener import custom_validators
from shortener.services import qr_generate


class Tag(models.Model):
    title = models.CharField('Название', max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Создатель тэга', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail', args=[self.title])


class Url(models.Model):
    full = models.CharField(max_length=300, verbose_name='Полный URL',
                            validators=[validators.URLValidator(message='Введите корректный адрес', code='invalid')])
    slug = models.CharField(max_length=50, verbose_name='Сокращённый URL', unique=True, blank=True,
                            error_messages={'unique': 'Укажите другой адрес'},
                            validators=[custom_validators.SlugValidator()])
    created = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    qr = models.FileField(upload_to='', blank=True, null=True)
    counter = models.IntegerField(verbose_name='Число переходов', default=0)
    last_redirect = models.DateField(auto_now_add=True, verbose_name='Дата последнего перехода')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)
    site_title = models.CharField(max_length=255, verbose_name='Заголовок сайта', blank=True, null=True)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Если поле "qr" пусто (при создании) или
        поле "qr" уже содержит файл отличный он нового "slug" (при редактировании),
        то генерируем новый qr-код
        """
        if self.qr.name is None or self.qr.name[0:-4] != self.slug:  # срез [0:-4] обозначает имя файла без '.png'
            img = qr_generate(self.slug)
            self.qr.delete(save=False)                               # удаляем старый qr-код
            self.qr.save(self.slug + '.png', BytesIO(img), save=False)
            super(Url, self).save(*args, **kwargs)
        else:
            super(Url, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('detail_url', args=[self.slug])

    def delete(self, *args, **kwargs):
        self.qr.delete(save=False)
        super().delete(*args, **kwargs)
