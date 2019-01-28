from django import template


register = template.Library()


class Groups(list):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def __contains__(self, element):
        return (
            self.user.is_superuser or
            super().__contains__('All') or
            super().__contains__(element)
        )


@register.simple_tag
def get_groups(user):
    groups = user.groups.values_list('name', flat=True)
    groups = Groups(user, groups)

    return groups
