from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog


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
        messagebox.showinfo("About", "Written by Stephan Martin\nVersion: 0.5\nDate: 26 March 2022")

    def report_call(self):
        NetReport()


class NetReport:
    # Report Page - pop open
    def __init__(self):
        self.report_window = Tk()
        self.report_window.title('Network Management Reports')
        self.report_window.attributes('-topmost', 1)
        self.report_frame = Frame(self.report_window)
        self.report_frame.grid(row=0, column=0, sticky=W+E)
        self.report_g1 = LabelFrame(self.report_frame, text="Select Options", padx=5, pady=5)
        self.report_g1.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(0, weight=1)
        self.report_g1.rowconfigure(0, weight=1)
        self.report_g1.columnconfigure(0, weight=1)

        self.reports_c1 = Checkbutton(self.report_g1, text='Hostname', onvalue=1, offvalue=0)
        self.reports_c1.grid(row=0, column=0, padx=15, pady=2, sticky=W)

        self.reports_c2 = Checkbutton(self.report_g1, text='IP Address', onvalue=1, offvalue=0)
        self.reports_c2.grid(row=1, column=0, padx=15, pady=2, sticky=W)

        self.reports_c3 = Checkbutton(self.report_g1, text='Serial Number', onvalue=1, offvalue=0)
        self.reports_c3.grid(row=2, column=0, padx=15, pady=2, sticky=W)

        self.reports_c4 = Checkbutton(self.report_g1, text='Version', onvalue=1, offvalue=0)
        self.reports_c4.grid(row=3, column=0, padx=15, pady=2, sticky=W)

        self.report_g2 = LabelFrame(self.report_frame, text="File input", padx=5, pady=5)
        self.report_g2.grid(row=4, column=0, padx=10, pady=10)
        self.report_window.columnconfigure(0, weight=1)
        self.report_window.rowconfigure(4, weight=1)
        self.report_g2.rowconfigure(4, weight=1)
        self.report_g2.columnconfigure(0, weight=1)

        self.reports_file = Button(self.report_g2, text='Select File', command=self.report_input)
        self.reports_file.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        self.report_run = Button(self.report_frame, text='Run')
        self.report_run.grid(row=5, column=0, padx=10, pady=10)

        self.txtbox = Text(self.report_g2, width=50, height=1)
        self.txtbox.grid(row=5, column=1, sticky=E + W + N + S)

        self.report_close = Button(self.report_frame, text='Close', command=self.report_window.destroy)
        self.report_close.grid(row=5, column=3, sticky=E, padx=15, pady=15)
        self.report_window.mainloop()

    def report_input(self):
        filename = filedialog.askopenfilename(parent=self.report_window, initialdir="/home/steve/Documents", title="Select source CSV", filetypes=(("CSV Files", "*.csv*"),
        ("all files", "*.*")))
        self.path_update(filename)

    def path_update(self, path):
        self.txtbox.insert(END, path)



# instantiate session
app = NetMain()
