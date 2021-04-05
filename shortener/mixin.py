from django.http import Http404


class AddRequestForFormInitMixin:
    """
    При инициализации формы добавляет в неё 'request'. Из него можем брать 'user', например.
    Смотри формы и их конструктор.
    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class GetObjectFromSlug:

    def get_object(self):
        model = self.model
        try:
            obj = model.objects.get(slug=self.kwargs['slug'])
            return obj
        except model.DoesNotExist:
            raise Http404
