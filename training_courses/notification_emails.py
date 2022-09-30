from django.core.mail import EmailMessage
from django.core import mail
from django.template import Context, Template
from django.conf import settings
import threading

execution_lock = threading.Lock()


def elearning_enquiry_notification(fullname, contact_num, msg):  
    with execution_lock:         
        html = Template('<!DOCTYPE html><html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Elearning Course Enquiry</title> </head> <body> <table><tr><td>Full Name</td><td>{}</td></tr><tr><td>Contact Number</td><td>{}</td></tr><tr><td>Message</td><td>{}</td></tr></table> </body></html>'.format(fullname, contact_num, msg))
        context = Context({})
        rendered_html = html.render(context)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            "Elearning Course Enquiry",
            rendered_html,
            settings.DEFAULT_FROM_EMAIL,
            ["daniel@driverhealth.co.za", "driverhealth2021@gmail.com", "ayatech.co@gmail.com"],
            reply_to=['admin@driverhealth.co.za'],
            headers={'Message-ID': 'DH00'},
            connection=connection
        )

        emailMsg.content_subtype = "html"
        emailMsg.send(fail_silently=False)