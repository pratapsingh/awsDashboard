#!/usr/bin/env python
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError
#from .models import SshRequest

def notification(subject, toadd, message, csrfile):
    groupemail = "no-reply@example.com"
    text_content = 'This is an important message!!'
    msg = EmailMultiAlternatives(subject, text_content, groupemail, [toadd, "devops@example.com"], reply_to=["devops@example.com"])
    fd = open(csrfile, 'r')
    msg.attach(csrfile, fd.read(), 'text/plain')
    msg.attach_alternative(message, "text/html")
    try:
        #send_mail(subject, msg, groupemail, [toadd,groupemail], reply_to="admin@example.com")
        msg.send()
    except BadHeaderError:
        print "Sendmail.notification: Bad header noticed"

def uploadNotification(subject, toadd, message):
    groupemail = "no-reply@example.com"
    text_content = 'This is an important message!!'
    msg = EmailMultiAlternatives(subject, text_content, groupemail, [toadd, "devops@example.com", "jira@example.com"], reply_to=["devops@example.com"])
    msg.attach_alternative(message, "text/html")
    try:
        #send_mail(subject, msg, groupemail, [toadd,groupemail], reply_to="admin@example.com")
        msg.send()
    except BadHeaderError:
        print "Sendmail.uploadNotification: Bad header noticed"
