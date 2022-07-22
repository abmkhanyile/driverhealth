from django import template

register = template.Library()

@register.simple_tag
def find_prev_next(days, counter):
    if counter < 10 and (days[counter] >= 20 and days[counter] <= 31):
        return 1
    elif counter > 15 and (days[counter] >= 1 and days[counter] <= days[len(days)-1]):
        return 2