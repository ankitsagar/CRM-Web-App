from django import template

register = template.Library()


@register.filter
def latest_task(taskset):
    if taskset:
        return taskset.latest('due_date')
    else:
        return None


