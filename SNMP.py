import getpass
import sys
import csv
import re
from pysnmp.hlapi import *
from pysnmp.smi.rfc1902 import ObjectIdentity



# Secure AutH/PRIV Storage

GET_AUTH = getpass.getpass('Enter Auth Passphrase: ')
GET_PRIV = getpass.getpass('Enter Priv Passphrase: ')

# SNMP Query Function


def get_info_snmp(host, oid):
    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
    UsmUserData('PYTHON_USR', authKey=GET_AUTH, privKey=GET_PRIV, authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb192Protocol),
    UdpTransportTarget((host, 161) , timeout = 3.0 , retries= 2),
    ContextData(),
    ObjectType(ObjectIdentity(oid)), lookupMib=False, lexicographicMode=False):

        if errorIndication:
            print(errorIndication, file=sys.stderr)

        elif errorStatus :
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)

        else:
            for varBind in varBinds:
                snmp_output = ('%s = %s' % varBind)
                snmp_output.strip("1.3.6.1.4.1.9.2.1.3.0 =")
                print(' = '.join([x.prettyPrint() for x in varBind]))


Addr_File = '/home/steve/Documents/Address.csv'

with open(Addr_File) as read_obj:
    datareader = csv.reader(read_obj)

    for row in datareader:
        # Strip brackets from list object
        raw_output = str(row)[1:-1]
        # Strip quotation from list obbject
        ipAddr = raw_output.strip("'")
        # Call list objects
        get_info_snmp(ipAddr, '1.3.6.1.4.1.9.2.1.3')
        #get_info_snmp(ipAddr, '1.3.6.1.2.1.1.1')


