from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import get_adapter as get_account_adapter

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.shortcuts import redirect
from django.contrib import messages
from allauth.socialaccount.models import SocialLogin

class MySocialAccount(DefaultSocialAccountAdapter):
        def pre_social_login(self, request, sociallogin):
                print request
                em = sociallogin.user.email
                print "============================\n"
                print em
                if not em.split('@')[1] == "example.com":
                        print "I am in if loop\n"
                        template = loader.get_template("error.html")
                        response = HttpResponse(template.render())
                        raise ImmediateHttpResponse(response)
                print "LOGS: Caught the signal--> Printing extra data of the acccount: \n", sociallogin.account.extra_data
#               default = DefaultSocialAccountAdapter()
#               return super(default, self).pre_social_login(request, sociallogin)
                return super(MySocialAccount, self).pre_social_login(request, sociallogin)

