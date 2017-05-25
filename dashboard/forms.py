from django import forms
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    domain = forms.CharField(label='Please enter domain name or URL : example.com or http://example.com/ ')
    docfile = forms.FileField(label='Upload certificate zip file of above domain')
    def clean_docfile(self):
        import os
        data = self.cleaned_data['docfile']
        print data
        ext = os.path.splitext(data.name)[1]  # [0] returns path+filename
        print "In validator function"
        print ext
        valid_extensions = ['.zip', '.tar', '.tar.gz', '.gz']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension. Upload only .zip, .tar.gz, .gz, .tar files only')
#        else:
#            filepath, filename = os.path.split(os.path.splitext(data.name)[0])
#            import zipfile
#            zip_ref = zipfile.ZipFile(os.path.splitext(data.name)[0], 'r')
#            zip_ref.extractall('/tmp')
#            zip_ref.close() 


        return data
     
    def clean_domain(self):
	from urlparse import urlparse
        import os, re
	domain = self.cleaned_data['domain']
	print domain
        if 'http' in domain:
                domain = urlparse(domain).hostname
        else:
                #pat="^(((([A-Za-z0-9]+){1,63}\.)|(([A-Za-z0-9]+(\-)+[A-Za-z0-9]+){1,63}\.))+){1,255}$"
		pat = "^(\*\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$"
                match = re.search(pat, domain)
                if match:
                        print "Valid domain name: %s" % (domain)
                else:
                        raise ValidationError(u'Invalid DomainName/URL provided. Please enter as "example.com"  or "http://example.com"')
	return domain
