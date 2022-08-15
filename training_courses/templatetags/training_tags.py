from datetime import datetime
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
def check_booking(day, month, year):
    date = datetime.date(year, month, day)
    # will retrieve events from a training day object
    trdays = TrainingDays.objects.filter(training_slot__date=date)

    events = []

    for trday in trdays:
        events.append(trday.trainingevent_set.all())
    
    eventdata = []
    # for event in events:
    #     eventdata.append(
    #         {
    #             'pk': event.pk,
    #             'trtimes': event.
    #         }
    #     )

    # for event in events:
    #     for eventdate in event.slots.all():
    #         if date == eventdate.training_slot.date():
    #             return


