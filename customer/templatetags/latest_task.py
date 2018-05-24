from django import template

register = template.Library()


@register.filter
def latest_task(taskset):
    if taskset:
        return taskset.latest('due_date')
    else:
        return None


@register.filter
def strip_str(string):
    print(string)
    if string:
        return string.strip()
    else:
        return None


