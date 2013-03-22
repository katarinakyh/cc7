"""
from django.dispatch import Signal

create_first_group_member = Signal(providing_args=['user', 'group', 'is_member'])

def model_saved(sender, **kwargs):
    print sender, kwargs


"""