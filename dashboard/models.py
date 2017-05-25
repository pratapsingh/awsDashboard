from __future__ import unicode_literals

from django.db import models
from django.core.validators import URLValidator
from .validators import validate_file_extension
from datetime import datetime

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(validators=[validate_file_extension], upload_to='documents/clientCertificates/%Y')
    domain_name = models.TextField(validators=[URLValidator()],default = 'null')
    emailId = models.CharField(max_length=50, default = 'null')
    tldr_name = models.CharField(max_length=60, default = 'null')
    uplaod_timestamp = models.DateTimeField(default=datetime.now, blank=True)

class CsrRequest(models.Model):
    domain_name = models.CharField(max_length=100, default = 'null')
    organization = models.CharField(max_length=60, default = 'null')
    department = models.CharField(max_length=60, default = 'null')
    city = models.CharField(max_length=100, default = 'null')
    state = models.CharField(max_length=100, default = 'null')
    country = models.CharField(max_length=60, default = 'null')
    keysize = models.CharField(max_length=60, default = 'null')
    admin_emailid = models.CharField(max_length=200, default = 'null')
    requester_emailid = models.CharField(max_length=200, default = 'null')
    csr_file_name = models.CharField(max_length=200, default = 'null')
    key_file_name = models.CharField(max_length=200, default = 'null')
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
