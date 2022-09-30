from datetime import datetime, date
from django import template
from training_courses.models import TrainingDays

register = template.Library()

@register.simple_tag
def find_prev_next(days, counter):
    if counter < 10 and (days[counter] >= 20 and days[counter] <= 31):
        return 1
    elif counter > 15 and (days[counter] >= 1 and days[counter] <= days[len(days)-1]):
        return 2


# this filter checks if a date is booked for training or not.
@register.simple_tag
def check_booking(cdate, trainingdates):
    event_num = []
    for trdate in trainingdates:
        if cdate == trdate.training_slot.date():
            event_num.append("a")
    return event_num


