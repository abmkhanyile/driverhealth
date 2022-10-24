from django import template
from driver_requests.models import Driver_Request

register = template.Library()

@register.simple_tag
def check_reqs(driver, company):
    driver_req = Driver_Request.objects.filter(driver=driver, company=company, closed=False)
    if driver_req.exists():
        return True
    else:
        return False
