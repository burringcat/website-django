from functools import partial

from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user and user.is_superuser


admin_required = partial(user_passes_test, test_func=is_admin)()