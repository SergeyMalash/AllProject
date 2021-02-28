from accounts.models import Account


def search_func(username, request_user):
    result = Account.objects.filter(username__icontains=username).exclude(username=request_user.username)
    return result
