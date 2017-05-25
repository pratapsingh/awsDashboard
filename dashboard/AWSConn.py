#/usr/bin/env python
import boto
from boto import ec2
from boto import rds2
from boto import connect_elb
from boto import connect_rds2
from boto import cloudtrail
import sys, os
#from django.conf import settings
sys.path.append('/app/devops/devops')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


PROFILES=["default"]
REGIONS=["ap-south-1", "eu-west-2", "eu-west-1", "ap-northeast-2", "ap-northeast-1", "sa-east-1", "ca-central-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2"]

#PROFILES = settings.AWS_PROFILES
#REGIONS = settings.AWS_REGIONS

def __init__(self):
	pass
def Ec2Conn(reg,profile = 'default'):
	ec2conn = ''
        try:
		ec2conn = boto.ec2.EC2Connection(profile_name=profile, region=boto.ec2.get_region(reg.strip()))
        except Exception, e:
		boto.log.error("Cannot validate provided AWS credentials: %s" % e)
	return(ec2conn)

def ELBConn(reg,profile = 'default'):
	endpt = 'elasticloadbalancing.' + reg + '.amazonaws.com'
	reg = boto.regioninfo.RegionInfo(name=reg,endpoint=endpt)
	elbconn = ''
	try:
		elbconn = boto.connect_elb(profile_name=profile, region=reg)
        except Exception, e:
                boto.log.error("Cannot validate provided AWS credentials: %s" % e)
        return(elbconn)

def RDSConn(reg,profile = 'default'):
	rdsconn = ''
	endpt = 'rds.' + reg + '.amazonaws.com'
	reg = boto.regioninfo.RegionInfo(name=reg,endpoint=endpt)
        try:
		rdsconn=boto.connect_rds2(profile_name=profile, region=reg)
        except Exception, e:
                boto.log.error("Cannot validate provided AWS credentials: %s" % e)
        return(rdsconn)
def CTRAILConn(reg, profile = 'defailt'):
	ctrail = ''
	endpt = 'cloudtrail.' + reg + '.amazonaws.com'	
	reg = boto.regioninfo.RegionInfo(name=reg,endpoint=endpt)
	try:
		ctrail = boto.connect_cloudtrail(profile_name=profile, region = reg)
	except Exception, e:
                boto.log.error("Cannot validate provided AWS credentials: %s" % e)
        return(ctrail)

def GetConn(contype = 'ec2', region = 'ap-southeast-1', profile = 'default'):
	if contype == 'ec2':
		ec2connection = Ec2Conn(region, profile)
		return(ec2connection)
	elif contype == 'elb':
		elbconnection = ELBConn(region, profile)
		return(elbconnection)
	elif contype == 'rds':
		rdsconnection = RDSConn(region, profile)
		return(rdsconnection)
	elif contype == 'cloudtrail':
		cdtrail = CTRAILConn(region, profile)
		return(cdtrail)
	else:
		raise ValueError('connection type -> contype <- must be from => ec2, elb, rds, cloudtrail')


if __name__=="__main__":
	GetConn(contype = 'ec2', region='ap-southeast-1', profile = 'default')
