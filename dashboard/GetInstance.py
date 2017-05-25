#!/usr/bin/python
from boto import ec2
from pprint import pprint
import boto, os, sys, errno, time
from math import log
import AWSConn
sys.path.append('/app/devops/devops')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

template_dir=settings.TEMPLATES[0]['DIRS'][0]

def Ec2Conn(reg, profile):
        try:
        	ec2conn = AWSConn.Ec2Conn(reg, profile)
        except Exception, e:
                log.error("Cannot validate provided AWS credentials: %s" % e)
        reservations = ec2conn.get_all_instances()
        instances = [i for r in reservations for i in r.instances]
        n = 1
        for j in instances:
        #        print n, j.id, j.ip_address, j.private_ip_address, j.state, j.vpc_id, j.subnet_id, j.dns_name, j.placement, j.tags
                convertHtml(reg, n, j.id, j.ip_address, j.private_ip_address, j.instance_type, j.state, j.vpc_id, j.key_name, j.dns_name, j.placement, j.tags, profile)
                n = n + 1
        ec2conn.close()
	mergefile(profile)

def GetInstance(profile):
        #clearing the file for the first time
        f = open('%s/%s.html' % (template_dir, profile), 'w+')
	f.close()
	h = open('%s/%s-temp.html' % (template_dir, profile), 'w')
	h.close()
        regions=settings.AWS_REGIONS
	for region in regions:
                connection = Ec2Conn(region, profile)

def convertHtml (region, n, instanceid, ipaddress, privateipaddress, instancetype, instancestate, vpcid, keyname, dnsname, availablilityzone, tags, profile):
        number = str(n)
        f = open('%s/%s-temp.html' % (template_dir, profile), 'a+')
        f.write('<div class="Row"> <div class="Cell"> <p>')
        f.write(number)
        f.write('</p> </div> <div class="Cell"> <p> ')
        f.write(instanceid)
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(str(ipaddress))
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(str(privateipaddress))
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(str(instancetype))
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(instancestate)
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(str(vpcid))
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(str(keyname))
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(dnsname)
        f.write('</p> </div> <div class="Cell"> <p>')
        f.write(availablilityzone)
        f.write('</p> </div> <div class="Cell"> <p>')
#        f.write(str(tags))
        for key,value in tags.iteritems():
                f.write('<b>')
                f.write("%s :" % (key))
                f.write('</b>')
                f.write("%s" % (value))
                f.write('<p></p>')
        f.write('</p> </div> </div>')
        f.write("\n")
        f.close()

def mergefile(profile):
        f = open('%s/%s.html' % (template_dir, profile), 'w')
        g = open('%s/%s-defaulttemplate.html' % (template_dir, profile), 'r+')
        h = open('%s/%s-temp.html' % (template_dir, profile), 'r+')
        updatedate = time.strftime("%d/%m/%Y")
        updatetime = time.strftime("%H:%M:%S")
	f.write ('<table style="width: 130%;"> <tr><td>')
        f.write('<b>Last Updated at</b> : Date : ')
        f.write(str(updatedate))
        f.write(' Time ')
        f.write(str(updatetime))
        f.write(' :: ')
	f.write('<td class="alignRight"> {% for account in user.socialaccount_set.all %} <p><b>User:</b> {{ user.email }}</p> {% endfor %} </td></tr> </table>')
        for lines in g.readlines():
                f.write(lines)
        g.close()
        for hlines in h.readlines():
                f.write(hlines)
        h.close()
        f.write("\n")
        f.write('</body>')
        f.write("\n")
        f.write('</html>')
        f.close()


if __name__=="__main__":
        #mkdir_p()
	try:
	       	profile = sys.argv[1]
	        GetInstance(profile)
	except IndexError:
		print "No Arg provided"
