from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog


def about():
    messagebox.showinfo("About", "Written by Stephan Martin\nVersion: 0.5\nDate: 26 March 2022")


def report_input():
    filename = filedialog.askopenfilename(initialdir="/", title="Select source CSV", filetypes=(("CSV Files", "*.csv*"),
    ("all files", "*.*")))


def reports():
    report_window = Tk()
    report_window.title('Reports')
    #report_window.wm_attributes('-topmost', 1)
    report_frame = Frame(report_window)
    report_frame.grid(row=0, column=0, sticky=W+E)
    report_g1 = LabelFrame(report_frame, text="Select Options", padx=5, pady=5)
    report_g1.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
    report_window.columnconfigure(0, weight=1)
    report_window.rowconfigure(0, weight=1)
    report_g1.rowconfigure(0, weight=1)
    report_g1.columnconfigure(0, weight=1)

    reports_c1 = Checkbutton(report_g1, text='Hostname', onvalue=1, offvalue=0)
    reports_c1.grid(row=0, column=0, padx=15, pady=2, sticky=W)

    reports_c2 = Checkbutton(report_g1, text='IP Address', onvalue=1, offvalue=0)
    reports_c2.grid(row=1, column=0, padx=15, pady=2, sticky=W)

    reports_c3 = Checkbutton(report_g1, text='Serial Number', onvalue=1, offvalue=0)
    reports_c3.grid(row=2, column=0, padx=15, pady=2, sticky=W)

    reports_c4 = Checkbutton(report_g1, text='Version', onvalue=1, offvalue=0)
    reports_c4.grid(row=3, column=0, padx=15, pady=2, sticky=W)

    report_g2 = LabelFrame(report_frame, text="File input", padx=5, pady=5)
    report_g2.grid(row=4, column=0, padx=10, pady=10)
    report_window.columnconfigure(0, weight=1)
    report_window.rowconfigure(4, weight=1)
    report_g2.rowconfigure(4, weight=1)
    report_g2.columnconfigure(0, weight=1)

    reports_file = Button(report_g1, text='Select File', command=report_input)
    reports_file.grid(row=5, column=0, padx=5, pady=5, sticky=W)

    report_run = Button(report_frame, text='Run')
    report_run.grid(row=5, column=0, padx=15, pady=15)

    #txtbox = scrolledtext.ScrolledText(group1, width=40, height=10)
    #txtbox.grid(row=0, column=0, sticky=E + W + N + S)

    report_close = Button(report_frame, text='Close', command=report_window.destroy)
    report_close.grid(row=5, column=3, sticky=E, padx=15, pady=15)
    report_window.mainloop()


def main():
    master_window = Tk()
    master_window.title('Network Management Tool')
    master_window.geometry("450x150")
    # Parent widget for the buttons
    buttons_frame = Frame(master_window)
    buttons_frame.grid(row=0, column=0, sticky=W+E)
    btn_reports = Button(buttons_frame, text='Reports', command=reports)
    btn_reports.grid(row=0, column=0, padx=15, pady=15)
    btn_file = Button(buttons_frame, text='Real Time Monitor')
    btn_file.grid(row=0, column=1, padx=15, pady=15)
    btn_about = Button(buttons_frame, text='About', command=about)
    btn_about.grid(row=0, column=3, padx=15, pady=15)
    btn_close = Button(buttons_frame, text='Close', command=master_window.destroy)
    btn_close.grid(row=0, column=4, padx=15, pady=15)
    mainloop()


main()
