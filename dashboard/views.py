#!/usr/bin/python -tt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.dispatch import Signal, receiver
from django.core.urlresolvers import reverse

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.signals import user_signed_up

import sys, os, json, time, unicodedata, SendMail, subprocess, GetInstance
from os import system

from .csrgen import generateCSR
from .models import Document, CsrRequest
from .forms import DocumentForm
from .SendMail import uploadNotification


# Create your views here.

def default(request):
        template = loader.get_template("index.html")
        return HttpResponse(template.render())

@login_required
@csrf_exempt
def dashboard(request):
        return render(request, 'loggedin.html', context = {"hi": "I want to print" })

@login_required
@csrf_exempt
def csrrequest(request,*args, **kwargs):
    if request.method == 'POST':
        if request.user.is_authenticated():
            username = request.user.email
            email = username
            fname = request.user.first_name
        print "I am in if loop"
        received_json_data=json.loads(request.body)
        data = request.body
        #Raw Data: "{"cname":"example.com","org":"test","department":"test","city":"test","stateProvince":"test","country":"IN","keySize":"2048","emailId":"admin@example.com"}"
        data = json.loads(data)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csrfile =  os.path.join('/app/csr-key', data['cname'] +'-'+ timestr + '.csr')
        keyfile = os.path.join('/app/csr-key', data['cname'] +'-'+ timestr + '.key')
        print 'Raw Data: "%s"' % request.body
        x = generateCSR(data,csrfile,keyfile)
        if x:
            Subject = "CSR Request :  %s" % (data['cname'])
#            Message = "<b>Hi Dear,</b><br></br><p>Your request for CSR generation for domain: %s was sucessful. Find the CSR in attached document.</p>" % (data['cname'])
            Message = "<b>Dear %s,</b><br></br><p>Your request for CSR generation for domain: %s was sucessful. Find the CSR in attached document.<br></br>Below information were provided to create CSR</p><br></br><b>Common Name:</b> %s<br></br><b>Organization:</b> %s<br></br><b>Oraganization Unit:</b> %s<br></br><b>Locality:</b> %s<br></br><b>State:</b> %s<br></br><b>Country:</b> %s<br></br><b>Key Size:</b> %s<br></br><b>Email:</b> %s<br></br> " % (fname, data['cname'], data['cname'], data['org'], data['department'], data['city'], data['stateProvince'], data['country'], data['keySize'], data['emailId'])
            #send email
            print "Sending email for CSR request"
            SendMail.notification(Subject, email, Message, csrfile)

            newdoc = CsrRequest(requester_emailid=request.user.email,domain_name=data['cname'], organization=data['org'], department=data['department'], city=data['city'], state=data['stateProvince'], country=data['country'], keysize=data['keySize'], admin_emailid=data['emailId'], csr_file_name=csrfile, key_file_name=keyfile)
            newdoc.save()

            return render(request, 'success.html', context = {'Success Check your email': "Sucess"})
        else :
            return render(request, 'success.html', context = {'Failure! Kindly check with Dev Ops team': 'Failure'})
    else :
        print "I am  in else loop"
        return render(request, 'csrreq.html', context = {"hi": "I want to print" })


#View for certificate upload
@login_required
@csrf_exempt
def list(request):
    # Handle file upload
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = DocumentForm(request.POST, request.FILES)
	print request.POST['domain']
        url = request.POST['domain']
	from urlparse import urlparse
	if 'http' in url:
		domain = urlparse(url).hostname
	else:
		domain = request.POST['domain']
        if form.is_valid():
            import tldextract
            host = tldextract.extract(domain)
            host = host.domain
            newdoc = Document(docfile=request.FILES['docfile'],emailId=request.user.email,domain_name=domain, tldr_name=host)
            newdoc.save()
            Subject = "Certificate file %s uploaded successfully for domain %s" % (request.FILES['docfile'], domain)
            Message = "<b>Dear %s,</b><br></br><p>Certificate file has been uploaded successfully.</p><br></br>Reach out to Dev Ops team for any further update.<br></br><br></br><b>DevOps:</p> A Jira issue has been created for SSL for the same</p><br></br><p></p>Thanks" % (request.user.first_name)
            uploadNotification(Subject, request.user.email, Message)
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all().order_by('-id')[:5] 

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )


@csrf_exempt
@login_required
def profile1(request):
    print request.method
    print "view profile1"
    if request.method == 'POST':
	GetInstance.GetInstance('PROFILE_1')
#	subprocess.Popen("/app/devops/dashboard/GetInstance.py PROFILE_1", shell=True)
        return render(request, 'PROFILE_1.html')
    else:
        return render(request, 'PROFILE_1.html')

@csrf_exempt
@login_required
def profile2(request):
    if request.method == 'POST':
	cmd="/app/devops/dashboard/GetInstance.py PROFILE_2"
        os.system(cmd)
        return render(request, 'PROFILE_2.html')
    else:
        return render(request, 'PROFILE_2.html')

@csrf_exempt
@login_required
def prodinstances(request):
    if request.method == 'POST':
	cmd="/app/devops/dashboard/GetInstance.py default"
        os.system(cmd)
        return render(request, 'default.html')
    else:
        return render(request, 'default.html')

