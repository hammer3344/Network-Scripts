from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import sys
import csv
import re

from pysnmp.hlapi import *
from pysnmp.smi.rfc1902 import ObjectIdentity


class NetMain:

    def __init__(self):
        # Main Window Session
        self.master_window = Tk()
        self.master_window.title('Network Management Tool')
        self.master_window.geometry("450x150")
        self.buttons_frame = Frame(self.master_window)
        self.buttons_frame.grid(row=0, column=0, sticky=W+E)
        self.btn_reports = Button(self.buttons_frame, text='Reports', command=self.report_call)
        self.btn_reports.grid(row=0, column=0, padx=15, pady=15)
        self.btn_file = Button(self.buttons_frame, text='Real Time Monitor')
        self.btn_file.grid(row=0, column=1, padx=15, pady=15)
        self.btn_about = Button(self.buttons_frame, text='About', command=self.about)
        self.btn_about.grid(row=0, column=3, padx=15, pady=15)
        self.btn_close = Button(self.buttons_frame, text='Close', command=self.master_window.destroy)
        self.btn_close.grid(row=0, column=4, padx=15, pady=15)
        mainloop()

    def about(self):
        messagebox.showinfo("About", "Written by Stephan Martin\nVersion: 0.8 Early Development\nDate: 26 March 2022")

    def report_call(self):
        NetReport()


class NetReport:
    # Report Page - pop open
    def __init__(self):
        self.report_window = Tk()
        self.report_window.title('Network Management Reports')
        self.report_window.attributes('-topmost', 1)
        self.report_frame = Frame(self.report_window)
        self.report_frame.grid(row=0, column=0, padx=5, pady=5, sticky=W+E)
        self.report_g1 = LabelFrame(self.report_frame, text="Select Options", padx=5, pady=5)
        self.report_g1.grid(row=0, column=0)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)
        self.report_g1.rowconfigure(0, weight=1)
        self.report_g1.columnconfigure(0, weight=1)

        self.reports_c1 = Checkbutton(self.report_g1, text='Hostname', onvalue=True, offvalue=False)
        self.reports_c1.grid(row=0, column=0, padx=5, pady=2, sticky=W)

        self.reports_c2 = Checkbutton(self.report_g1, text='IP Address', onvalue=True, offvalue=False)
        self.reports_c2.grid(row=1, column=0, padx=5, pady=2, sticky=W)

        self.reports_c3 = Checkbutton(self.report_g1, text='Serial Number', onvalue=True, offvalue=False)
        self.reports_c3.grid(row=2, column=0, padx=5, pady=2, sticky=W)

        self.reports_c4 = Checkbutton(self.report_g1, text='Version', onvalue=True, offvalue=False)
        self.reports_c4.grid(row=3, column=0, padx=5, pady=2, sticky=W)

        # SNMP Credential Frame
        self.report_g2 = LabelFrame(self.report_frame, text="SNMP Credentials", padx=5, pady=5)
        self.report_g2.grid(row=0, column=1, padx=10, pady=10)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)
        self.report_g2.rowconfigure(0, weight=1)
        self.report_g2.columnconfigure(0, weight=1)

        # SNMP Credential objects
        self.snmp_usr_label = Label(self.report_g2, text='SNMP User:')
        self.snmp_usr_label.grid(row=0, column=0, padx=5, pady=5)
        self.snmp_usr = Text(self.report_g2, width=30, height=1)
        self.snmp_usr.grid(row=0, column=1, padx=5, pady=5)
        self.snmp_sha_label = Label(self.report_g2, text='SNMP Auth:')
        self.snmp_sha_label.grid(row=1, column=0, padx=5, pady=5)
        self.snmp_sha = Entry(self.report_g2, show='*', width=30)
        self.snmp_sha.grid(row=1, column=1, padx=5, pady=5)
        self.snmp_aes_label = Label(self.report_g2, text='SNMP Priv:')
        self.snmp_aes_label.grid(row=2, column=0, padx=5, pady=5)
        self.snmp_aes = Entry(self.report_g2, show='*', width=30)
        self.snmp_aes.grid(row=2, column=1, padx=5, pady=5)

        # File Select frame
        self.report_g3 = LabelFrame(self.report_frame, text="File Input", padx=5, pady=5)
        self.report_g3.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)
        self.report_g3.rowconfigure(0, weight=1)
        self.report_g3.columnconfigure(0, weight=1)

        # File Select objects
        self.reports_file = Button(self.report_g3, text='Select File', command=self.report_input)
        self.reports_file.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.txtbox = Text(self.report_g3, width=50, height=1)
        self.txtbox.grid(row=0, column=2, sticky=E + W + N + S)

        # File Output Frame
        self.report_g4 = LabelFrame(self.report_frame, text="File Output Path", padx=5, pady=5)
        self.report_g4.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)
        self.report_g4.rowconfigure(0, weight=1)
        self.report_g4.columnconfigure(0, weight=1)

        # File output objects
        self.reports_file_select = Button(self.report_g4, text='Select Destination:', command=self.report_output)
        self.reports_file_select.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.txtbox_output = Text(self.report_g4, width=50, height=1)
        self.txtbox_output.grid(row=0, column=2, sticky=E + W + N + S)

        # Run or close
        self.report_run = Button(self.report_frame, text='Run', command=self.csv_processing)
        self.report_run.grid(row=3, column=0, padx=5, pady=5, sticky=E)

        self.report_close = Button(self.report_frame, text='Close', command=self.report_window.destroy)
        self.report_close.grid(row=3, column=1, sticky=E, padx=5, pady=5)

        self.oid_hostname = '1.3.6.1.4.1.9.2.1.3'
        self.oid_sn = '1.3.6.1.2.1.47.1.1.1.1.11'
        self.oid_ver = '1.3.6.1.2.1.1.1'

        self.report_window.mainloop()

    def report_input(self):
        filename = filedialog.askopenfilename(parent=self.report_window, initialdir="/home/steve/Documents",
                                              title="Select source CSV", filetypes=(("CSV Files", "*.csv*"),
                                                                                    ("all files", "*.*")))
        self.path_update(filename)

    def path_update(self, path):
        self.txtbox.insert(END, path)

    def report_output(self):
        filename = filedialog.askdirectory(parent=self.report_window, initialdir="/home/steve/Documents",
                                           title="Select output path")
        self.output_update(filename)
        self.output_file(filename)

    def output_update(self, path):
        self.txtbox_output.insert(END, path)

    def output_file(self, file):
        filename = file

    def snmp_process(self, host, oid):

        #user_pre = self.snmp_usr.get("1", END)
        #user_post = user_pre.strip("\n")
        #auth_pre = self.snmp_sha.get("1", END)
        #auth_post = auth_pre.strip("\n")

        #priv_pre = self.snmp_aes.get("1", END)
        #priv_post = priv_pre.strip("\n")
        # SNMP Process Generation
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
             UsmUserData('PYTHON_USR', authKey='PythonSHA', privKey='PythonAES',
             authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb192Protocol),
             UdpTransportTarget((host, 161), timeout=3.0, retries=2),
             ContextData(),
             ObjectType(ObjectIdentity(oid)), lookupMib=False, lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'),
                      file=sys.stderr)

            else:
                for varBind in varBinds:
                    output = str('%s = %s' % varBind)
                    return output
                    #messagebox.showinfo("SNMP Complete", "SNMP string built")

    def csv_processing(self):

        addr_pre = self.txtbox.get("1.0", END)
        addr_file = addr_pre.strip("\n")

    # MIB request and report writer
        with open(addr_file) as read_obj:
            datareader = csv.reader(read_obj)

            for row in datareader:
                # Strip brackets from list object
                raw_output = str(row)[1:-1]
                # Strip quotation from list object
                ipaddr = raw_output.strip("'")

                output_list = []
                version_list = []
                final_list = []

            # Hostname MIB + output processing
                while self.reports_c1:
                    hostname_mib = self.snmp_process(ipaddr, '1.3.6.1.4.1.9.2.1.3')
                    hostname_output = hostname_mib.replace('1.3.6.1.4.1.9.2.1.3.0 = ', '')
                    output_list.append(hostname_output)
                    self.reports_c1 = False
                    #messagebox.showinfo("report c1", "callback complete")

                while self.reports_c2:
                    output_list.append(ipaddr)
                    #messagebox.showinfo("report c2", "callback complete")
                    self.reports_c2 = False

                while self.reports_c3:
                    # Serial Number MIB + output processing
                    serial_mib = self.snmp_process((str(ipaddr)), '1.3.6.1.2.1.47.1.1.1.1.11')
                    serial_output = serial_mib.replace('1.3.6.1.2.1.47.1.1.1.1.11.1 = ', '')
                    output_list.append(serial_output)
                    self.reports_c3 = False
                    #messagebox.showinfo("report c3", "callback complete")

                while self.reports_c4:
                    # Version MIB + output processing
                    version_mib = self.snmp_process((str(ipaddr)), '1.3.6.1.2.1.1.1')
                    version_match = re.findall('Cisco.+', version_mib)
                    version_clean = str(version_match)[1:-1]
                    version_strip = version_clean.strip("'")
                    version_list = version_strip.split(', ')
                    final_list = output_list + version_list
                    self.reports_c4 = False
                    #messagebox.showinfo("report c4", "callback complete")

            #final_list = output_list + version_list

            # Write CSV File
            csv_pre = self.txtbox_output.get("1.0", END)
            csv_post = '/home/steve/Documents/output.csv'
            csv_write = open(csv_post, 'a', newline='')
        with csv_write:
            write = csv.writer(csv_write)
            write.writerow(final_list)
            csv_write.close()
            #messagebox.showinfo("report csv", "callback complete")

        #messagebox.showinfo("Report Complete")

app = NetMain()
