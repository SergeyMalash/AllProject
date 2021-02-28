from django.db import models


class AnonDialog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField('AnonMessages')
    users = models.ManyToManyField('AnonUser')
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return '.'.join(self.users.values_list('channel_name', flat=True))


class AnonMessages(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200, blank=False, null=False)
    dialog = models.ForeignKey('AnonDialog', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('AnonUser', on_delete=models.CASCADE, null=True)


class AnonUser(models.Model):

    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    AGE = [
        ('1', 'до 18 лет'),
        ('2', 'от 18 до 21 года'),
        ('3', 'от 22 до 25 лет'),
        ('4', 'от 26 до 30 лет'),
        ('5', 'больше 30 лет')
    ]
    gender = models.CharField(max_length=6, choices=GENDER)
    age = models.CharField(max_length=1, choices=AGE)
    is_available = models.BooleanField(default=True)
    channel_name = models.CharField(max_length=100)
