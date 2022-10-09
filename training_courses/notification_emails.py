from django.core.mail import EmailMessage
from django.core import mail
from django.template import Context, Template
from django.conf import settings
import threading

execution_lock = threading.Lock()


def elearning_enquiry_notification(fullname, contact_num, email_addr, msg):  
    with execution_lock:         
        html = Template('<!DOCTYPE html><html lang="en"> <head> <meta charset="UTF-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Elearning Course Enquiry</title> </head> <body> <table><tr><td>Full Name</td><td>{}</td></tr><tr><td>Contact Number</td><td>{}</td></tr><tr><td>Email Address</td><td>{}</td></tr><tr><td>Message</td><td>{}</td></tr></table> </body></html>'.format(fullname, contact_num, email_addr, msg))
        context = Context({})
        rendered_html = html.render(context)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            "Course Enquiry",
            rendered_html,
            settings.DEFAULT_FROM_EMAIL,
            ["daniel@driverhealth.co.za", "driverhealth2021@gmail.com", "ayatech.co@gmail.com"],
            reply_to=['admin@driverhealth.co.za'],
            headers={'Message-ID': 'DH00'},
            connection=connection
        )

        emailMsg.content_subtype = "html"
        emailMsg.send(fail_silently=False)

# sends an email to confirm the booking for training.
def booking_confirmation(cname, trans):  
    with execution_lock:         
        html = Template('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elearning Course Enquiry</title></head><body><h5 class="text-success">Booking successful</h5><h5 class="text-danger">{}</h5><p>Please make a payment within the next 48 hours to confirm your booking. Use<span class="text-danger">{}</span>as a reference for the payment.</p><p>You can make a payment into the following bank account</p><table class="table table-sm"><tr><td>Account Holder</td><td>DriverHealth Africa (PTY) LTD</td></tr><tr><td>Bank</td><td>ABSA</td></tr><tr><td>Account Number</td><td>41-0505-4532</td></tr><tr><td>Clearing Code</td><td>632005</td></tr><tr><td>Referrence</td><td>{}</td></tr></table><h3 class="text-success">Amount to Pay: R{}</h3></body></html>'.format(cname, trans.trans_id, trans.trans_id, trans.trans_tot))
        context = Context({})
        rendered_html = html.render(context)

        connection = mail.get_connection()
        emailMsg = EmailMessage(
            "Booking Confirmation",
            rendered_html,
            settings.DEFAULT_FROM_EMAIL,
            ["daniel@driverhealth.co.za", "driverhealth2021@gmail.com", "ayatech.co@gmail.com"],
            reply_to=['admin@driverhealth.co.za'],
            headers={'Message-ID': 'DH00'},
            connection=connection
        )

        emailMsg.content_subtype = "html"
        emailMsg.send(fail_silently=False)