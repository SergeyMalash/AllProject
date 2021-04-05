from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class SlugValidator:
    """Проверяет заданный slug и запрещает некоторые из них"""
    def __call__(self, val):
        if val in ['api', 'api-auth', 'todo', 'account', 'messenger', 'admin', 'slug', 'urls', 'tags', 'user',
                   'anonymous', 'blog', 'search'
                   ]:
            raise ValidationError('Такой адрес задать нельзя', code='forbidden')

        all_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for sym in val:
            if sym not in all_symbols:
                raise ValidationError('Допустимы только буквы и цифры', code='invalid')
