#!/usr/bin/env python
#
# Generate a key, self-signed certificate, and certificate request.
# Usage: csrgen <fqdn>
#
# When more than one hostname is provided, a SAN (Subject Alternate Name)
# certificate and request are generated.  This can be acheived by adding -s.
# Usage: csrgen <hostname> -s <san0> <san1>
#
# Author: Courtney Cotton <cotton@cottoncourtney.com> 06-25-2014

# Libraries/Modules

from OpenSSL import crypto
import os.path

# Generate Certificate Signing Request (CSR)
def generateCSR(data,csrfile,keyfile):
    #data is json similar to Raw Data: "{"cname":"test","org":"test","department":"tests","city":"tes","stateProvince":"testes","country":"tsetse","keySize":"2048","emailId":"est"}"
    print data
    print "================================================="
    print "In generateCSR function"
    print type(data)
    print "================================================="
#    csrfile = data['cname'].csr
 #   keyfile = data['cname'].key
#    csrfile = os.path.join('/app/devops/csr-key', data['cname'] + '.csr')
#    keyfile = os.path.join('/app/devops/csr-key', data['cname'] + '.key')
    TYPE_RSA = crypto.TYPE_RSA

    req = crypto.X509Req()
    req.get_subject().CN = data['cname']
    req.get_subject().countryName = data['country']
    req.get_subject().stateOrProvinceName = data['stateProvince']
    req.get_subject().localityName = data['city']
    req.get_subject().organizationName = data['org']
    req.get_subject().organizationalUnitName = data['department']
    req.get_subject().emailAddress = data['emailId']
    # Add in extensions
    base_constraints = ([
        crypto.X509Extension("keyUsage", False, "Digital Signature, Non Repudiation, Key Encipherment"),
        crypto.X509Extension("basicConstraints", False, "CA:FALSE"),
    ])
    x509_extensions = base_constraints
    req.add_extensions(x509_extensions)
    # Utilizes generateKey function to kick off key generation.
    key = generateKey(TYPE_RSA, int(data['keySize']))
    req.set_pubkey(key)

    #update sha?
    #req.sign(key, "sha1")
    req.sign(key, "sha256")

    generateFiles(csrfile, req)
    generateFiles(keyfile, key)
    print "I am going to return True\n" 
    return True
#    return req

# Generate Private Key
def generateKey(type, bits):

    key = crypto.PKey()
    key.generate_key(type, bits)
    return key

# Generate .csr/key files.
def generateFiles(mkFile, request):

    if '.csr' in mkFile:
        f = open(mkFile, "w")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, request))
        f.close()
        print crypto.dump_certificate_request(crypto.FILETYPE_PEM, request)
    elif '.key' in mkFile:
        f = open(mkFile, "w")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, request))
        f.close()
    else:
        print "Failed."
        exit()
