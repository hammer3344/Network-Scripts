import getpass
import sys
import csv
import re
from pysnmp.hlapi import *
from pysnmp.smi.rfc1902 import ObjectIdentity



# Secure AutH/PRIV Storage

GET_USER = getpass.getuser('Enter SNMP User: ')
GET_AUTH = getpass.getpass('Enter Auth Passphrase: ')
GET_PRIV = getpass.getpass('Enter Priv Passphrase: ')


#SNMP Function
def get_info_snmp(host, oid):
    for (errorIndication,errorStatus,errorIndex,varBinds) in nextCmd(SnmpEngine(),
    UsmUserData(GET_USER, authKey=GET_AUTH, privKey=GET_PRIV, authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb192Protocol),
    UdpTransportTarget((host, 161), timeout=3.0, retries=2),
    ContextData(),
    ObjectType(ObjectIdentity(oid)), lookupMib=False, lexicographicMode=False):

        if errorIndication:
            print(errorIndication, file=sys.stderr)

        elif errorStatus :
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)

        else:
            for varBind in varBinds:
                output = (str('%s = %s' % varBind))
                return output


# Define address list file path
Addr_File = '/home/steve/Documents/Address.csv'

# MIB request and report writer
with open(Addr_File) as read_obj:
    datareader = csv.reader(read_obj)

    for row in datareader:
        # Strip brackets from list object
        raw_output = str(row)[1:-1]
        # Strip quotation from list obbject
        ipAddr = raw_output.strip("'")

        # Hostname MIB + output processing
        hostname_mib = get_info_snmp(ipAddr, '1.3.6.1.4.1.9.2.1.3')
        hostname_output = hostname_mib.replace('1.3.6.1.4.1.9.2.1.3.0 = ', '')
        output_list = []
        output_list.append(hostname_output)
        output_list.append(ipAddr)

        # Serial Number MIB + output processing
        serial_mib = get_info_snmp(ipAddr, '1.3.6.1.2.1.47.1.1.1.1.11')
        serial_output = serial_mib.replace('1.3.6.1.2.1.47.1.1.1.1.11.1 = ', '')
        output_list.append(serial_output)


        # Version MIB + output processing
        version_mib = get_info_snmp(ipAddr, '1.3.6.1.2.1.1.1')
        version_match = re.findall('Cisco.+', version_mib)
        version_clean = str(version_match)[1:-1]
        version_strip = version_clean.strip("'")
        version_list = version_strip.split(', ')
        final_list = output_list + version_list

        #Write CSV File
        csv_write = open('/home/steve/Documents/output.csv', 'a', newline='')
        with csv_write:
            write = csv.writer(csv_write)
            write.writerow(final_list)
            csv_write.close()
