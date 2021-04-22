"""

Notes by nitin murarkar Sir

Normal days & Known Event the Hit Ratio is high 65% to 70%
On Expiry & Friday & VIX > 25 & Gap up & Gap down openiing >2% & Sudden Event : The Lower Hit Ratio 55% to 60%

Golden Rules

Trade after 10:30 am
pre defines stop loss in terms of Rs, 1800-200 per lot
Trade ATM/ITM (Delta 0.5 to 0.7) Intraday
Always use Stop loss is most important
rule of profit booking 20 to 40 points
avoide over levraging
Equal lot in every trade month 
do not hold naked index weekly option in loss more than 2 days
Carry forward only hedged position like spreds (bull/bear)

Odin percentage
chnage of OI % with respect to OI



"""



from tkinter import *
from tkinter.ttk import Combobox , Button
from tkinter import messagebox
import tksheet
import pandas
import datetime
from dateutil.relativedelta import relativedelta
import webbrowser
import csv
import requests
import sys
import streamtologger
import numpy
import os
import itertools

# imports for graph
from PIL import ImageTk,Image
import matplotlib.pyplot as plt


# noinspection PyAttributeOutsideInit
class NseOI:
    def __init__(self, window: Tk):
        # Starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        # print(Starttime)
        self.seconds = 60
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.previous_date = None
        self.previous_time = None
        self.first_run = True
        self.stop = False
        self.logging = False
        self.dates = [""]
        self.indices = ["BANKNIFTY","NIFTY","FINNIFTY"]
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) '
                                      'Chrome/80.0.3987.149 Safari/537.36',
                        'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
        self.url_oc = "https://www.nseindia.com/option-chain"
        self.session = requests.Session()
        self.cookies = {}
        self.login_win(window)

    def get_data(self, event=None):
        if self.first_run:
            return self.get_data_first_run()
        else:
            return self.get_data_refresh()

    def get_data_first_run(self):
        request = None
        response = None
        self.index = self.index_var.get()
        try:
            url = f"https://www.nseindia.com/api/option-chain-indices?symbol={self.index}"
            request = self.session.get(self.url_oc, headers=self.headers, timeout=5)
            self.cookies = dict(request.cookies)
            response = self.session.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
        except Exception as err:
            #print(request)
            #print(response)
            print('NSE Site data pull error 1')
            #print(err, "1")
            messagebox.showerror(title="Error", message="Error in fetching dates.\nPlease retry.")
            self.dates.clear()
            self.dates = [""]
            self.date_menu.config(values=tuple(self.dates))
            ## Date featching errors 
            self.date_menu.current(0)
            return
        
        if response is not None:
            try:
                json_data = response.json()
            except Exception as err:
                #print(response)
                print('NSE Site data pull error 2')
                #print(err, "2")
                json_data = {}
        else:
            json_data = {}
        if json_data == {}:
            messagebox.showerror(title="Error", message="Error in fetching dates.\nPlease retry.")
            self.dates.clear()
            self.dates = [""]
            try:
                self.date_menu.config(values=tuple(self.dates))
                self.date_menu.current(0)
            except TclError as err:
                #print(err, "3")
                print('NSE Site data pull error 3')
                
            return
        self.dates.clear()
        for dates in json_data['records']['expiryDates']:
            self.dates.append(dates)
        try:
            self.date_menu.config(values=tuple(self.dates))
            self.date_menu.current(0)
        except TclError as err:
            #print(err, "4")
            print('NSE Site data pull error 4')

        return response, json_data

    def get_data_refresh(self):
        request = None
        response = None
        try:
            url: str = f"https://www.nseindia.com/api/option-chain-indices?symbol={self.index}"
            response = self.session.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
            if response.status_code == 401:
                self.session.close()
                self.session = requests.Session()
                url = f"https://www.nseindia.com/api/option-chain-indices?symbol={self.index}"
                request = self.session.get(self.url_oc, headers=self.headers, timeout=5)
                self.cookies = dict(request.cookies)
                response = self.session.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
                print("reset cookies")
        except Exception as err:
            #print(request)
            #print(response)
            print('NSE Site data pull error 4')
            #print(err, "4")
            try:
                self.session.close()
                self.session = requests.Session()
                url = f"https://www.nseindia.com/api/option-chain-indices?symbol={self.index}"
                request = self.session.get(self.url_oc, headers=self.headers, timeout=5)
                self.cookies = dict(request.cookies)
                response = self.session.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
                print("reset cookies")
            except Exception as err:
                #print(request)
                #print(response)
                print('NSE Site data pull error 5',self.str_current_time)
                #print(err, "5")
                return
        if response is not None:
            try:
                json_data = response.json()
            except Exception as err:
                #print(response)
                print('NSE Site data pull error 6')
                #print(err, "6")
                json_data = {}
        else:
            json_data = {}
        if json_data == {}:
            return

        return response, json_data

    def login_win(self, window: Tk):
        self.login = window
        self.login.title("NSE")
        window_width = self.login.winfo_reqwidth()
        window_height = self.login.winfo_reqheight()
        position_right = int(self.login.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.login.winfo_screenheight() / 2 - window_height / 2)
        self.login.geometry("320x110+{}+{}".format(position_right, position_down))

        self.index_var = StringVar()
        self.index_var.set(self.indices[0])
        self.dates_var = StringVar()
        self.dates_var.set(self.dates[0])

        index_label = Label(self.login, text="Index: ", justify=LEFT)
        index_label.grid(row=0, column=0, sticky=N + S + W)
        self.index_menu = Combobox(self.login, textvariable=self.index_var, values=self.indices)
        self.index_menu.config(width=15)
        self.index_menu.grid(row=0, column=1, sticky=N + S + E)
        date_label = Label(self.login, text="Expiry Date: ", justify=LEFT)
        date_label.grid(row=1, column=0, sticky=N + S + E)
        self.date_menu = Combobox(self.login, textvariable=self.dates_var)
        self.date_menu.config(width=15)
        self.date_menu.grid(row=1, column=1, sticky=N + S + E)
        self.date_get = Button(self.login, text="Refresh", command=self.get_data)
        self.date_get.grid(row=1, column=2, sticky=N + S + E)
        sp_label = Label(self.login, text="Strike Price: ")
        sp_label.grid(row=2, column=0, sticky=N + S + E)
        self.sp_entry = Entry(self.login, width=18)
        self.sp_entry.grid(row=2, column=1, sticky=N + S + E)
        start_btn = Button(self.login, text="Start", command=self.start)
        start_btn.grid(row=2, column=2, sticky=N + S + E + W)
        self.sp_entry.focus_set()
        self.get_data()

        def focus_widget(event, mode: int):
            if mode == 1:
                self.get_data()
                self.date_menu.focus_set()
            elif mode == 2:
                self.sp_entry.focus_set()

        self.index_menu.bind('<Return>', lambda event, a=1: focus_widget(event, a))
        self.index_menu.bind("<<ComboboxSelected>>", self.get_data)
        self.date_menu.bind('<Return>', lambda event, a=2: focus_widget(event, a))
        self.sp_entry.bind('<Return>', self.start)

        self.login.mainloop()

    def start(self, event=None):
        self.expiry_date = self.dates_var.get()
        if self.expiry_date == "":
            messagebox.showerror(title="Error", message="Incorrect Expiry Date.\nPlease enter correct Expiry Date.")
            return
        try:
            self.sp = int(self.sp_entry.get())
            self.login.destroy()
            self.main_win()
        except ValueError as err:
            print(err, "8")
            messagebox.showerror(title="Error", message="Incorrect Strike Price.\nPlease enter correct Strike Price.")

    def change_state(self, event=None):

        if not self.stop:
            self.stop = True
            self.options.entryconfig(self.options.index(0), label="Start")
            print("Data pull stop")
            messagebox.showinfo(title="Stopped", message="Scraping new data has been stopped.")
        else:
            self.stop = False
            self.options.entryconfig(self.options.index(0), label="Stop")
            print("Data pull started")
            messagebox.showinfo(title="Started", message="Scraping new data has been started.")

            self.main()

    def export(self, event=None):
        from datetime import date ,datetime
        pdate = datetime.now().strftime("%d-%m-%Y")
        sheet_data = self.sheet.get_sheet_data()
        csv_exists: bool = os.path.isfile(f"OptionChain-{self.index}-Exp-{self.expiry_date}-Date-{pdate}.csv")
        try:
            if not csv_exists:
                with open(f"OptionChain-{self.index}-Exp-{self.expiry_date}-Date-{pdate}.csv", "a", newline="") as row:
                    data_writer: csv.writer = csv.writer(row)
                    data_writer.writerow(('Time', 'Spot Price', 'Call_CHOI\n(in K)', 'Put_CHOI\n(in K)', 'CHOI_Diff\n(in K)', 'M3Call_CHOI\n(in K)',
            'M3Put_CHOI\n(in K)', 'M3CHOI_Diff\n(Put - Call)', 'Diff_Max3_CHOI\n(Put - Call)'))
            
            with open(f"OptionChain-{self.index}-Exp-{self.expiry_date}-Date-{pdate}.csv", "a", newline="") as row:
                data_writer: csv.writer = csv.writer(row)
                data_writer.writerows(sheet_data)

            messagebox.showinfo(title="Export Successful",
                                message=f"Data has been exported to OptionChain-{self.index}-Exp-{self.expiry_date}-Date-{pdate}.csv")
        except Exception as err:
            print(err, "9")
            messagebox.showerror(title="Export Failed",
                                 message="An error occurred while exporting the data.")

    def log(self, event=None):
        if not self.logging:
            streamtologger.redirect(target="nse.log", header_format="[{timestamp:%Y-%m-%d %H:%M:%S} - {level:5}] ")
            self.logging = True
            self.options.entryconfig(self.options.index(2), label="Logging: On")
            messagebox.showinfo(title="Started", message="Debug Logging has been enabled.")
        elif self.logging:
            sys.stdout = self.stdout
            sys.stderr = self.stderr
            streamtologger._is_redirected = False
            self.logging = False
            self.options.entryconfig(self.options.index(2), label="Logging: Off")
            messagebox.showinfo(title="Stopped", message="Debug Logging has been disabled.")

    
    def close(self, event=None):
        ask_quit = messagebox.askyesno("Quit", "All unsaved data will be lost.\nProceed to quit?", icon='warning',
                                       default='no')
        if ask_quit:
            self.session.close()
            self.root.destroy()
            sys.exit()
        elif not ask_quit:
            pass
    
    def toggle(self,event=None):
        if self.toggleb_b == "Start":
            self.toggleb_b = "Stop"
            messagebox.showerror(title="Live Graph Stoped",
                                 message="Live Graph Stoped")
            #print("Tfun_l1",self.toggleb_b)
        else:
            self.toggleb_b = "Start"
            messagebox.showinfo(title="Live Graph Started",
                                 message="Live Graph Started")
            #print("Tfun_2",self.toggleb_b)
            
            
    # def graphs1(self,event=None):
    #     sheet_data = self.sheet.get_sheet_data()
    #     df_sd = pandas.DataFrame(sheet_data)
    #     #print (df_sd)
    #     CHOI_PLOT = df_sd.plot(x=0,y=4,label = "CH_OI_Diff")
    #     plt.xlabel('Time')
    #     plt.ylabel('CH_OI_Diff')
    #     plt.legend()
    #     plt.show()
        
    def graphsAll(self,event=None):
        #Create figure window
        fig, axes = plt.subplots(nrows=3, ncols=3)
        
        sheet_data = self.sheet.get_sheet_data()
        df_sd = pandas.DataFrame(sheet_data)
        df_sd[9] = df_sd[5]+df_sd[6]
        df_sd[10] = df_sd[3]/df_sd[2]
        #print (df_sd)
        #"CH_OI_Diff" graph
        CHOI_PLOT = df_sd.plot(x=0,y=4,label = "CH_OI_Diff" , ax=axes[0,0])
        
        # Volume base CHOI difference graph
        OI_Diff_PLOT = df_sd.plot(x=0,y=7,label = "MVol3_CHOI_D",ax=axes[0,1])
        
        # CH_OI PCR difference graph
        CH_OI_PCR_PLOT = df_sd.plot(x=0,y=10,label = "CH_OI_PCR",ax=axes[2,0])
        
        #Diffrance of  Volume difference graph
        volume_Diff_PLOT = df_sd.plot(x=0,y=8,label = "Diff_Volume",ax=axes[0,2])
 
        #Long Short count graph
        #time_data = self.time_count
        # long_data = self.long_count
        # short_data = self.short_count
        # ls_data = {'Time':time_data,'Long':long_data,'Short':short_data}
        # df_ls = pandas.DataFrame(ls_data)
        # #print (df_ls)
        # LS_PLOT = df_ls.plot(x=0,y=[1,2],ax=axes[1,1])
        

       
        #Price action Graph
        # price_data = self.price_count
        # pa_data = {'Time':time_data,'Price_Action':price_data}
        # df_pa = pandas.DataFrame(pa_data)
        # PA_PLOT = df_pa.plot(x=0,y=1,label = 'Price_Action',ax=axes[2,2])
        
        # LTP graph
        LTP_PLOT = df_sd.plot(x=0,y=1,label = "LTP",ax=axes[2,1])
        plt.xlabel('Time')
        
        ## IV Graph
        time_ivdata = self.time_iv
        civ_data = self.tciv_list
        piv_data = self.tpiv_list
        iv_data = {'Time':time_ivdata,'Call_IV':civ_data,'Put_IV':piv_data}
        df_iv = pandas.DataFrame(iv_data)
        #print (df_iv)
        iv_PLOT = df_iv.plot(x=0,y=[1,2],ax=axes[1,2])
       
        ## OI Graph
        time_data = self.time_count
        OI_data = self.totaOI

        oi_dataf = {'Time':time_data,'Total_OI':OI_data}
        df_OI = pandas.DataFrame(oi_dataf)
        
        oi_PLOT = df_OI.plot(x=0,y=1,ax=axes[1,0])
        
        
        #plt.legend()
        plt.show()



    
    def program1(self,event=None):
        import NIFTY_BANKNIFTY_ML_Regration_BOT_Auto_Class as ml_prog
        print("ML_Reg_Program Start")
        ml_reg_auto = ml_prog.ML_Reg.ml_regration_auto()  
        # print("PCB_Program")
        # nf50_bn_pcb= ml_prog.ML_Reg.nf_bn_pcb()
        messagebox.showinfo(title="ML Program", message="Machine learning Reg program exported the Data to csv files.")
        print("ML_Reg Program_End")

    def program2(self,event=None):
        #Curently takeing offline as not working #
        import FOI_BN_NF_ML_Classification__Level2_BOT_FR1 as ml_classifi
        print("ML_Classi_Program_Start")
        ml_class_auto = ml_classifi.ML_classi.ml_classification()
        messagebox.showinfo(title="ML_Classi Program", message="Machine learning Classi program exported the Data to csv files.")
        print("ML_Classi Program_End")
        
    def main_win(self):
        self.root = Tk()
        self.root.focus_force()
        self.root.title("Option-Chain-Analyzer")
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 3 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 3 - window_height / 2)
        self.root.geometry("815x510+{}+{}".format(position_right, position_down))
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        
        menubar = Menu(self.root)
        self.options = Menu(menubar, tearoff=0)
        self.options.add_command(label="Stop", command=self.change_state)
        self.options.add_separator()
        self.options.add_command(label="Export to CSV", command=self.export)
        #self.options.add_command(label="Logging: Off   (Ctrl+L)", command=self.log)
        self.options.add_separator()
        self.options.add_command(label="All_Graph", command=self.graphsAll)
        self.options.add_separator()
        self.options.add_command(label="Live Graph Start/Stop", command=self.toggle)
        self.options.add_separator()
        self.options.add_command(label="Machine_Learning_SR", command=self.program1)
        #self.options.add_command(label="Machine_Learning_Classi", command=self.program2)
        self.options.add_separator()
        
        self.options.add_command(label="Quit", command=self.close)
        menubar.add_cascade(label="Menu", menu=self.options)
        self.root.config(menu=menubar)

        # self.root.bind('<Control-s>', self.export)
        # self.root.bind('<Control-l>', self.log)
        # self.root.bind('<Control-x>', self.change_state)
        
        # self.root.bind('<Control-q>', self.close)

        top_frame = Frame(self.root)
        top_frame.rowconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)
        top_frame.pack(fill="both", expand=True)
        
        #output_columns names

        output_columns = ('Time', 'Spot Price', 'Call_CHOI\n(in K)', 'Put_CHOI\n(in K)', 'CHOI_Diff\n(Put - Call)', 'M3Call_OI\n(in K)',
            'M3Put_OI\n(in K)', 'M3_CHOI_Diff\n(Put - Call)', 'Diff_Volume\n(Put - Call)')
        
        ##orignal_columns_names = ['Time', 'Value', 'Call Sum\n(in K)', 'Put Sum\n(in K)', 
         #'Difference\n(in K)', 'Call Boundary\n(in K)', 'Put Boundary\n(in K)', 'Call ITM', 'Put ITM']
        
        ## Names are change as per new program modification refer the Backup program for correct Names
        self.sheet = tksheet.Sheet(top_frame, column_width=85, align="center", headers=output_columns,
                                   header_font=("TkDefaultFont", 10, "bold"), empty_horizontal=0,
                                   empty_vertical=20, header_height=35)
        self.sheet.enable_bindings(("toggle_select", "drag_select", "column_select", "row_select", "column_width_resize",
             "arrowkeys", "right_click_popup_menu", "rc_select", "select_all"))
        self.sheet.grid(row=0, column=0, sticky=N + S + W + E)

        bottom_frame = Frame(self.root)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.rowconfigure(1, weight=1)
        bottom_frame.rowconfigure(2, weight=1)
        bottom_frame.rowconfigure(3, weight=1)
        bottom_frame.rowconfigure(4, weight=1)
        bottom_frame.rowconfigure(5, weight=1)
        bottom_frame.rowconfigure(6, weight=1)
        bottom_frame.rowconfigure(7, weight=1)
        bottom_frame.rowconfigure(8, weight=1)
        bottom_frame.rowconfigure(9, weight=1)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.columnconfigure(3, weight=1)
        bottom_frame.columnconfigure(4, weight=1)
        bottom_frame.columnconfigure(5, weight=1)
        bottom_frame.columnconfigure(6, weight=1)
        bottom_frame.columnconfigure(7, weight=1)
        bottom_frame.pack(fill="both", expand=True)


        # oi_lb_label = Label(bottom_frame, text="OCA Program imp Data", relief=RIDGE,
        #                     font=("TkDefaultFont", 10, "bold"))
        # oi_lb_label.grid(row=0, column=0, columnspan=4, sticky=N + S + W + E)

        current_Time_label = Label(bottom_frame, text="Sys_Update_Time:", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        current_Time_label.grid(row=0, column=4, sticky=N + S + W + E)
            
        self.current_time_val = Label(bottom_frame, text="", relief=RIDGE)
        self.current_time_val.grid(row=0, column=5, sticky=N + S + W + E)
        
        diff_Time_label = Label(bottom_frame, text="Time_Diff:", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        diff_Time_label.grid(row=0, column=6, sticky=N + S + W + E)
        
        self.diff_Time_val = Label(bottom_frame, text="", relief=RIDGE,font=("TkDefaultFont", 10, "bold"))
        self.diff_Time_val.grid(row=0, column=7, sticky=N + S + W + E)    
        
        max_call_oi_sp_label = Label(bottom_frame, text="Max Call OI:", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        max_call_oi_sp_label.grid(row=1, column=0, sticky=N + S + W + E)
        
        self.max_call_oi_sp_val = Label(bottom_frame, text="", relief=RIDGE)
        self.max_call_oi_sp_val.grid(row=1, column=1, sticky=N + S + W + E)
        
        max_call_oi_label = Label(bottom_frame, text="OI (in K):", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        max_call_oi_label.grid(row=1, column=2, sticky=N + S + W + E)
        
        self.max_call_oi_val = Label(bottom_frame, text="", relief=RIDGE)
        self.max_call_oi_val.grid(row=1, column=3, sticky=N + S + W + E)
        
        # oi_lb_label = Label(bottom_frame, text="Max Put OI", relief=RIDGE,
        #                     font=("TkDefaultFont", 10, "bold"))
        # oi_lb_label.grid(row=0, column=4, columnspan=4, sticky=N + S + W + E)
        
        max_put_oi_sp_label = Label(bottom_frame, text="Max Put OI:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        max_put_oi_sp_label.grid(row=1, column=4, sticky=N + S + W + E)
        
        self.max_put_oi_sp_val = Label(bottom_frame, text="", relief=RIDGE)
        self.max_put_oi_sp_val.grid(row=1, column=5, sticky=N + S + W + E)
        
        max_put_oi_label = Label(bottom_frame, text="OI (in K):", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        max_put_oi_label.grid(row=1, column=6, sticky=N + S + W + E)
        
        self.max_put_oi_val = Label(bottom_frame, text="", relief=RIDGE)
        self.max_put_oi_val.grid(row=1, column=7, sticky=N + S + W + E)
        
        ## ITM Intrinsic value time value
        #Call
        ITM_call_val_sp_label = Label(bottom_frame, text="Call ITM SP", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        ITM_call_val_sp_label.grid(row=6, column=0, sticky=N + S + W + E)
        
        self.ITM_call_val_sp_val = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_call_val_sp_val.grid(row=6, column=1, sticky=N + S + W + E)
        
        ITM_call_val_label = Label(bottom_frame, text="Call PreV:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        ITM_call_val_label.grid(row=6, column=2, sticky=N + S + W + E)
        
        self.ITM_call_val_val = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_call_val_val.grid(row=6, column=3, sticky=N + S + W + E)

        ITM_call_inv_label = Label(bottom_frame, text="C_ITM_InV", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        ITM_call_inv_label.grid(row=7, column=0, sticky=N + S + W + E)
        
        self.ITM_call_inv = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_call_inv.grid(row=7, column=1, sticky=N + S + W + E)
        
        ITM_call_Tval_label = Label(bottom_frame, text="C_ITM_Tval:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        ITM_call_Tval_label.grid(row=7, column=2, sticky=N + S + W + E)
        
        self.ITM_call_Tval = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_call_Tval.grid(row=7, column=3, sticky=N + S + W + E)
        
        #Put
        ITM_put_val_sp_label = Label(bottom_frame, text="Put ITM SP", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        ITM_put_val_sp_label.grid(row=6, column=4, sticky=N + S + W + E)
        
        self.ITM_put_val_sp_val = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_put_val_sp_val.grid(row=6, column=5, sticky=N + S + W + E)
        
        ITM_put_val_label = Label(bottom_frame, text="Put PreV:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        ITM_put_val_label.grid(row=6, column=6, sticky=N + S + W + E)
        
        self.ITM_put_val_val = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_put_val_val.grid(row=6, column=7, sticky=N + S + W + E)

        ITM_put_inv_label = Label(bottom_frame, text="P_ITM_InV", relief=RIDGE,
                                     font=("TkDefaultFont", 10, "bold"))
        ITM_put_inv_label.grid(row=7, column=4, sticky=N + S + W + E)
        
        self.ITM_put_inv = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_put_inv.grid(row=7, column=5, sticky=N + S + W + E)
        
        ITM_put_Tval_label = Label(bottom_frame, text="P_ITM_Tval:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        ITM_put_Tval_label.grid(row=7, column=6, sticky=N + S + W + E)
        
        self.ITM_put_Tval = Label(bottom_frame, text="", relief=RIDGE)
        self.ITM_put_Tval.grid(row=7, column=7, sticky=N + S + W + E)
        
        
                
        
        ##
        max_call_oi_sp_2_label = Label(bottom_frame, text="Spot Op LTP:", relief=RIDGE,
                                              font=("TkDefaultFont", 9, "bold"))
        max_call_oi_sp_2_label.grid(row=2, column=0, sticky=N + S + W + E)
        
        self.max_call_oi_sp_2_val= Label(bottom_frame, text="", relief=RIDGE)
        self.max_call_oi_sp_2_val.grid(row=2, column=1, sticky=N + S + W + E)
        
        max_call_oi_2_label= Label(bottom_frame, text="Spot Op IV:", relief=RIDGE,
                                           font=("TkDefaultFont", 9, "bold"))
        max_call_oi_2_label.grid(row=2, column=2, sticky=N + S + W + E)
        
        self.max_call_oi_2_val= Label(bottom_frame, text="", relief=RIDGE)
        self.max_call_oi_2_val.grid(row=2, column=3, sticky=N + S + W + E)
        

        
        max_put_oi_sp_2_label= Label(bottom_frame, text="Spot Op LTP:", relief=RIDGE,
                                             font=("TkDefaultFont", 9, "bold"))
        max_put_oi_sp_2_label.grid(row=2, column=4, sticky=N + S + W + E)
        
        self.max_put_oi_sp_2_val= Label(bottom_frame, text="", relief=RIDGE)
        self.max_put_oi_sp_2_val.grid(row=2, column=5, sticky=N + S + W + E)
        
        max_put_oi_2_label= Label(bottom_frame, text="Spot Op IV:", relief=RIDGE,
                                          font=("TkDefaultFont", 9, "bold"))
        max_put_oi_2_label.grid(row=2, column=6, sticky=N + S + W + E)
        
        self.max_put_oi_2_val= Label(bottom_frame, text="", relief=RIDGE)
        self.max_put_oi_2_val.grid(row=2, column=7, sticky=N + S + W + E)

        ##
        
        # oi_label = Label(bottom_frame, text="CH_OI_Suggetion:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        # oi_label.grid(row=3, column=0, columnspan=2, sticky=N + S + W + E)
        
        # self.oi_val = Label(bottom_frame, text="", relief=RIDGE)
        # self.oi_val.grid(row=3, column=2, columnspan=2, sticky=N + S + W + E)
        
        pcr_label = Label(bottom_frame, text="TF_CHOI_PCR:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        pcr_label.grid(row=0, column=0, columnspan=2, sticky=N + S + W + E)
        
        self.pcr_val = Label(bottom_frame, text="", relief=RIDGE)
        self.pcr_val.grid(row=0, column=2, columnspan=2, sticky=N + S + W + E)
        
        ## 
        # call_exits_label = Label(bottom_frame, text="OI_Long_Short:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        # call_exits_label.grid(row=4, column=0, columnspan=2, sticky=N + S + W + E)
        
        # self.call_exits_val = Label(bottom_frame, text="", relief=RIDGE)
        # self.call_exits_val.grid(row=4, column=2, columnspan=2, sticky=N + S + W + E)
        
        # put_exits_label = Label(bottom_frame, text="Price action Count:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        # put_exits_label.grid(row=4, column=4, columnspan=2, sticky=N + S + W + E)
        
        # self.put_exits_val = Label(bottom_frame, text="", relief=RIDGE)
        # self.put_exits_val.grid(row=4, column=6, columnspan=2, sticky=N + S + W + E)
        
        # call_itm_label = Label(bottom_frame, text="Long Count:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        # call_itm_label.grid(row=5, column=0, columnspan=2, sticky=N + S + W + E)
        
        # self.call_itm_val = Label(bottom_frame, text="", relief=RIDGE)
        # self.call_itm_val.grid(row=5, column=2, columnspan=2, sticky=N + S + W + E)
        
        # put_itm_label = Label(bottom_frame, text="Short Count:", relief=RIDGE, font=("TkDefaultFont", 10, "bold"))
        # put_itm_label.grid(row=5, column=4, columnspan=2, sticky=N + S + W + E)
        
        # self.put_itm_val = Label(bottom_frame, text="", relief=RIDGE)
        # self.put_itm_val.grid(row=5, column=6, columnspan=2, sticky=N + S + W + E)

        self.root.after(100, self.main)

        self.root.mainloop()

    def get_dataframe(self):
        try:
            
            response, json_data = self.get_data()
        except TypeError:
            return
        if response is None or json_data is None:
            return

        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.width', 400)

        df = pandas.read_json(response.text)
        df = df.transpose()

        ce_values = [data['CE'] for data in json_data['records']['data'] if
                     "CE" in data and str(data['expiryDate'].lower() == str(self.expiry_date).lower())]
        pe_values = [data['PE'] for data in json_data['records']['data'] if
                     "PE" in data and str(data['expiryDate'].lower() == str(self.expiry_date).lower())]
        underlying_stock = ce_values[0]['underlying']
        self.underlying_name = ce_values[0]['underlying']
        
        points : float = pe_values[0]['underlyingValue']
        if points == 0:
            for item in range (len(ce_values)):
                points : float = ce_values[item]['underlyingValue']
                if points != 0:
                    break
        #print(len(ce_values))
        # ##Second solution
        # if points == 0:
        #     for item in pe_values:
        #         if item['underlyingValue'] != 0:
        #             points = item['underlyingValue']
        #             break
                
            
        #print((points))
        #print(underlying_stock)
        ce_data = pandas.DataFrame(ce_values)
        pe_data = pandas.DataFrame(pe_values)
        ce_data_f = ce_data.loc[ce_data['expiryDate'] == self.expiry_date]
        pe_data_f = pe_data.loc[pe_data['expiryDate'] == self.expiry_date]
        if ce_data_f.empty:
            messagebox.showerror(title="Error",
                                 message="Invalid Expiry Date.\nPlease restart and enter a new Expiry Date.")
            self.change_state()
            return
        columns_ce = ['openInterest', 'changeinOpenInterest', 'totalTradedVolume', 'impliedVolatility', 'lastPrice',
                      'change', 'bidQty', 'bidprice', 'askPrice', 'askQty', 'strikePrice']
        columns_pe = ['strikePrice', 'bidQty', 'bidprice', 'askPrice', 'askQty', 'change', 'lastPrice',
                      'impliedVolatility', 'totalTradedVolume', 'changeinOpenInterest', 'openInterest']
        ce_data_f = ce_data_f[columns_ce]
        pe_data_f = pe_data_f[columns_pe]
        merged_inner = pandas.merge(left=ce_data_f, right=pe_data_f, left_on='strikePrice', right_on='strikePrice')
        merged_inner.columns = ['Open Interest', 'Change in Open Interest', 'Traded Volume', 'Implied Volatility',
                                'Last Traded Price', 'Net Change', 'Bid Quantity', 'Bid Price', 'Ask Price',
                                'Ask Quantity', 'Strike Price', 'Bid Quantity', 'Bid Price', 'Ask Price',
                                'Ask Quantity', 'Net Change', 'Last Traded Price', 'Implied Volatility',
                                'Traded Volume', 'Change in Open Interest', 'Open Interest']
        return merged_inner, df['timestamp']['records'], underlying_stock, points


    def set_values(self):
        ## Logic for the displaying values on window
        self.root.title(f"OCA- {self.underlying_stock} - {self.expiry_date} - {self.sp}")

        self.max_call_oi_val.config(text=self.max_call_oi)
        self.max_call_oi_sp_val.config(text=self.max_call_oi_sp)
        self.max_put_oi_val.config(text=self.max_put_oi)
        self.max_put_oi_sp_val.config(text=self.max_put_oi_sp)
        
        self.max_call_oi_2_val.config(text=self.max_call_oi_2)
        self.max_call_oi_sp_2_val.config(text=self.max_call_oi_sp_2)
        self.max_put_oi_2_val.config(text=self.max_put_oi_2)
        self.max_put_oi_sp_2_val.config(text=self.max_put_oi_sp_2)
        
        self.current_time_val_text = datetime.datetime.now().strftime("%H:%M:%S") 
        self.current_time_val.config(text=self.current_time_val_text)
        
        self.diff_Time_val.config(text=format(self.minutes ,'.2f'))
        
    
        self.ITM_call_val_sp_val.config(text=self.call_ITM_Stp)
        self.ITM_call_val_val.config(text=self.call_ITM_pre)
        self.ITM_call_inv.config(text=self.call_itm_Int)
        self.ITM_call_Tval.config(text=self.call_itm_Tval)
        
        self.ITM_put_val_sp_val.config(text=self.put_ITM_Stp)
        self.ITM_put_val_val.config(text=self.put_ITM_pre)
        self.ITM_put_inv.config(text=self.put_itm_Int)
        self.ITM_put_Tval.config(text=self.put_itm_Tval)
        
        

        red = "#f7ebeb"
        green = "#ebf7f5"
        default = "SystemButtonFace"
        
        # initalizing empty lists
        # long_list = []
        # short_list = []
        # call_list =[]
        # put_list = []

        
        #int_put = 0  #if needed uncomment
        #int_call = 0


            
        
        if self.put_call_ratio >= 1:
            self.pcr_val.config(text=format(self.put_call_ratio,'.2f'), bg=green)
        else:
            self.pcr_val.config(text=format(self.put_call_ratio,'.2f'), bg=red)

        def set_itm_labels(call_change: float, put_change: float) -> str:
            label = "NA"
            if put_change > call_change:
                if put_change >= 0:
                    if call_change <= 0:
                        label = "NA"
                    elif put_change / call_change > 1.5:
                        label = "NA"
                else:
                    if put_change / call_change < 0.5:
                        label = "NA"
            if call_change <= 0:
                label = "NA"
            return label

      
    
        output_values = [self.str_current_time, self.points, self.call_sum, self.put_sum, self.difference,
                         self.call_boundary, self.put_boundary, self.call_itm, self.put_itm]
        
        self.sheet.insert_row(values=output_values)

        last_row = self.sheet.get_total_rows() - 1

        # Logic for CH_OI table colour background change

        # if self.first_run or self.points == self.old_points:
        #     self.old_points = self.points
        # elif self.points > self.old_points:
        #     self.sheet.highlight_cells(row=last_row, column=1, bg=green)
        #     #self.old_points = self.points
        #     int_call = 1
        #     call_list.append(int_call)
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=1, bg=red)
        #     #self.old_points = self.points
        #     int_put = -1
        #     put_list.append(int_put)
        
        

        ## Put call old and current logic
        
        # if self.first_run or self.old_call_sum == self.call_sum:
        #     self.old_call_sum = self.call_sum
        # elif self.call_sum > self.old_call_sum:
        #     self.sheet.highlight_cells(row=last_row, column=2, bg=green)
            
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=2, bg=red)
        #     #self.old_call_sum = self.call_sum
        
        
        # if self.first_run or self.old_put_sum == self.put_sum:
        #     self.old_put_sum = self.put_sum
        # elif self.put_sum > self.old_put_sum:
        #     self.sheet.highlight_cells(row=last_row, column=3, bg=green)
            
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=3, bg=red)
        #     #self.old_put_sum = self.put_sum

        # if self.first_run or self.old_difference == self.difference:
        #     self.old_difference = self.difference
        # elif self.difference > self.old_difference:
        #     self.sheet.highlight_cells(row=last_row, column=4, bg=green)
        #     #self.old_difference = self.difference
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=4, bg=red)


        # if (self.put_sum > self.old_put_sum):
        #     if (self.call_sum < self.old_call_sum):
        #         if (self.old_difference < self.difference):
        #             self.oi_val.config(text="Buy CE", bg=green)
        #             int_long = 1
        #             long_list.append(int_long)
        # elif (self.put_sum < self.old_put_sum) :
        #     if (self.call_sum > self.old_call_sum):
        #         if (self.old_difference > self.difference):
        #             self.oi_val.config(text="Buy PE", bg=red)
        #             int_short = 1
        #             short_list.append(int_short)
        # else:
        #     self.oi_val.config(text="Hold", bg=red)
              
        
        # if self.first_run or self.old_call_boundary == self.call_boundary:
        #     self.old_call_boundary = self.call_boundary
        # elif self.call_boundary > self.old_call_boundary:
        #     self.sheet.highlight_cells(row=last_row, column=5, bg=green)
        #     #self.old_call_boundary = self.call_boundary
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=5, bg=red)
        #     #self.old_call_boundary = self.call_boundary
        
        
        # if self.first_run or self.old_put_boundary == self.put_boundary:
        #     self.old_put_boundary = self.put_boundary
        # elif self.put_boundary > self.old_put_boundary:
        #     self.sheet.highlight_cells(row=last_row, column=6, bg=green)
        #     #self.old_put_boundary = self.put_boundary
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=6, bg=red)
        #     #self.old_put_boundary = self.put_boundary
        
        # # Call and put vLong Short ## Change the Call_Exit lable in above display
        
        # ## Temp solution for BankNifty LTP Zero value
        # if self.points == 0 :
        #     self.points = self.sp
                        
        # if (self.points > self.old_points) and ((self.call_boundary + self.put_boundary) > (self.old_call_boundary + self.old_put_boundary)) :
        #     self.call_exits_val.config(text= "Long Bulidup" , bg=green)
        #     int_long = 1
        #     long_list.append(int_long)
        # elif (self.points > self.old_points) and ((self.call_boundary + self.put_boundary) < (self.old_call_boundary + self.old_put_boundary)) :
        #     self.call_exits_val.config(text= "Short Covering" , bg=green)
        #     int_long = 1
        #     long_list.append(int_long)
        # elif (self.points < self.old_points) and ((self.call_boundary + self.put_boundary) < (self.old_call_boundary + self.old_put_boundary)) :
        #     self.call_exits_val.config(text= "Long Unwinding" , bg=red)
        #     int_short = 1
        #     short_list.append(int_short)
        # elif (self.points < self.old_points) and ((self.call_boundary + self.put_boundary) > (self.old_call_boundary + self.old_put_boundary)) :
        #     self.call_exits_val.config(text= "Short Buildup" , bg=red)
        #     int_short = 1
        #     short_list.append(int_short)
        # elif self.first_run :
        #     self.call_exits_val.config(text= "First Run" , bg=green)
        # else:
        #     self.call_exits_val.config(text= "No Change" , bg=green)
        
        

        # ## ITM cell logic
            
        # if self.first_run or self.old_call_itm == self.call_itm:
        #     self.old_call_itm = self.call_itm
        # elif self.call_itm > self.old_call_itm:
        #     self.sheet.highlight_cells(row=last_row, column=7, bg=green)
        #     #self.old_call_itm = self.call_itm
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=7, bg=red)
        #     #self.old_call_itm = self.call_itm
        
        
        # if self.first_run or self.old_put_itm == self.put_itm:
        #     self.old_put_itm = self.put_itm
        # elif self.put_itm > self.old_put_itm:
        #     self.sheet.highlight_cells(row=last_row, column=8, bg=green)
        #     #self.old_put_itm = self.put_itm
        # else:
        #     self.sheet.highlight_cells(row=last_row, column=8, bg=red)
        #     #self.old_put_itm = self.put_itm
            
        # if self.first_run or self.old_put_itm == self.put_itm:
        #     self.old_put_itm = self.put_itm
        # elif (abs(self.put_itm) < abs(self.old_put_itm)*0.5):
        #     self.sheet.highlight_cells(row=last_row, column=8, bg=red)
        #     #messagebox.showinfo(title="Volume difference", message="50 % Down difference given in Volume")
        # elif (abs(self.put_itm) > abs(self.old_put_itm)*1.5):
        #     self.sheet.highlight_cells(row=last_row, column=8, bg=green)
        #     #messagebox.showinfo(title="Volume difference", message="50 % difference given in Volume")
            
        # #print("New,old ",abs(self.put_itm),abs(self.old_put_itm))
        
        # if self.first_run :
        #     # self.old_total_short = 0
        #     # self.old_total_long = 0
        #     self.old_total_put = 0
        #     self.old_total_call = 0
        
        
        # total_long = sum(long_list)+0
        # total_short = sum(short_list)+0
        
        # self.new_total_long = total_long + self.old_total_long
        # self.new_total_short = total_short + self.old_total_short
        
        
        # first run empty Lists for graph & logic
        if self.first_run :
            self.time_count = []
            # self.long_count = []
            # self.short_count = []
            # self.price_count = []
            self.price_mml = []
            self.bm = []

        
        self.time_count = self.time_count
        # self.long_count = self.long_count
        # self.short_count = self.short_count
        # self.price_count = self.price_count
        self.price_mml = self.price_mml
        self.bm = self.bm+[0]
 
            
        self.time_count.append(self.str_current_time)
        # self.long_count.append(self.new_total_long)
        # self.short_count.append(self.new_total_short)
        self.price_mml.append(self.points)
        
        try:
            if ((max(self.price_mml)-min(self.price_mml))/max(self.price_mml))*100 > 2:
                #print("\n")                   
                if sum(self.bm) <= 3:
                    messagebox.showinfo(title="Big Move", message="Price move near 2%")
                    bmp = 1
                    self.bm.append(bmp)
                    print("Index Price move near 2%")
                  
        
        except ZeroDivisionError:
            print("Error in NSE option chain data")
            
        
        ## Total long short count output
        
        # self.call_itm_val.config(text= self.new_total_long, bg=default)
        # self.put_itm_val.config(text= self.new_total_short, bg=default)
        
        
        ## Price action logic
        # total_call = sum(call_list)+0
        # total_put = sum(put_list)+0
        
        # new_total_call = total_call + self.old_total_call
        # new_total_put = total_put + self.old_total_put
        
        # total_price_action = new_total_call + new_total_put
        ## put_exit column 
        # self.put_exits_val.config(text= total_price_action , bg=default)
        # self.price_count.append(total_price_action)
        #Updating the new data to old data ##IMP
        self.old_points = self.points
        self.old_put_sum = self.put_sum
        self.old_call_sum = self.call_sum
        self.old_put_boundary = self.put_boundary
        self.old_call_boundary = self.call_boundary
        self.old_call_itm = self.call_itm
        self.old_put_itm = self.put_itm
        # self.old_total_long = self.new_total_long
        # self.old_total_short = self.new_total_short
        # self.old_total_call = new_total_call
        # self.old_total_put = new_total_put
        self.old_difference = self.difference
        
        #print(self.points)
        ## Req. a stop function
        ## Logic for graph

        if self.first_run:
            self.toggleb_b = "Start"
        #print(self.toggleb_b)
        
        if self.toggleb_b == "Start":
            sheet_data = self.sheet.get_sheet_data()
            df_sd = pandas.DataFrame(sheet_data)
            if self.first_run is not True:
                plt.close()
            
            # INITIALIZE FIG DIMENSION AND AXES OBJECTS
            fig, axs = plt.subplots(figsize=(8,4))
    
            # ASSIGN AXES OBJECTS ACCORDINGLY
            df_sd.plot(ax=axs, x=0, y=7, label='M3CHOI_Diff', grid=True,  linewidth=2) #
            df_sd.plot(ax=axs, x=0, y=1, secondary_y=True, label='Index', linewidth=1) #
            
            
            # CHOI_PLOT = df_sd.plot(x=0,y=4,label = "CH_OI_Diff")
            plt.xlabel('Time')
            plt.ylabel('M3CH_OI_Diff')
            plt.title(self.index)
            #plt.legend()
            plt.show()
            #print("Data append loop")
        
        if self.sheet.get_yview()[1] >= 0.9:
            self.sheet.see(last_row)
            self.sheet.set_yview(1)
        self.sheet.refresh()

    def main(self):
        if self.stop:
            return

        try:
            df, current_time, self.underlying_stock, self.points = self.get_dataframe()
        except TypeError:
            self.root.after((self.seconds * 360), self.main)
            return

        
        #print(self.points)
        if self.underlying_name == "NIFTY" :
            rval = 50
        else:
            rval = 100
        #print(self.underlying_name)
        if self.points != 0:
            self.spotprice = int(rval * round(float(self.points)/rval))
            #print(self.spotprice)
        else:
            self.spotprice = self.sp
        
        ## Logic for ITM StP
        if self.underlying_name == "NIFTY" :
            self.call_ITM_Stp = self.spotprice-50
            self.put_ITM_Stp = self.spotprice+50
        else:
            self.call_ITM_Stp = self.spotprice-100
            self.put_ITM_Stp = self.spotprice+100
        
        #ITM Index
        self.call_ITM_index = int(df[df['Strike Price'] == self.call_ITM_Stp].index.tolist()[0])
        #print("call",self.call_ITM_Stp)
        self.put_ITM_index = int(df[df['Strike Price'] == self.put_ITM_Stp].index.tolist()[0])
        #print("put",self.put_ITM_Stp)
        
        self.call_ITM_pre = df.iloc[self.call_ITM_index]['Last Traded Price'][0]
        self.put_ITM_pre = df.iloc[self.put_ITM_index]['Last Traded Price'][1]
        
        self.call_itm_Int = int(abs(float(self.points)-self.call_ITM_Stp))
        self.put_itm_Int = int(abs(float(self.points)-self.put_ITM_Stp))

        self.call_itm_Tval = int(self.call_ITM_pre-self.call_itm_Int)
        self.put_itm_Tval = int(self.put_ITM_pre-self.put_itm_Int)
        

  
        ## Time diff logic
        os_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        os_update_time = datetime.datetime.strptime(os_time, '%Y-%m-%d %H:%M:%S')
        #os_HMS = datetime.datetime.strptime(os_time, '%H:%M:%S')
        
        opc_time = current_time
        opc_time_update = datetime.datetime.strptime(opc_time, '%d-%b-%Y %H:%M:%S')

        diff_time = os_update_time - opc_time_update
        self.minutes = diff_time.total_seconds() / 60
        #print(self.minutes)
        if self.first_run:
            print("First Run")
            print("Current Program is running for: ",self.underlying_stock)
        elif self.minutes >= 3:
            messagebox.showinfo(title="Time difference", message="Time difference is more than 5 min")
                
        
        self.str_current_time = current_time.split(" ")[1]        
        current_date = datetime.datetime.strptime(current_time.split(" ")[0], '%d-%b-%Y').date()
        current_time = datetime.datetime.strptime(current_time.split(" ")[1], '%H:%M:%S').time()
  
        
        if self.first_run:
            self.previous_date = current_date
            self.previous_time = current_time
        elif current_date > self.previous_date:
            self.previous_date = current_date
            self.previous_time = current_time
        elif current_date == self.previous_date:
            if current_time > self.previous_time:
                self.previous_time = current_time
            else:
                self.root.after((self.seconds * 360), self.main)
                return

        call_oi_list = []
        for i in range(len(df)):
            int_call_oi = int(df.iloc[i, [0]][0])
            call_oi_list.append(int_call_oi)
        call_oi_index = call_oi_list.index(max(call_oi_list))
        self.max_call_oi = round(max(call_oi_list) / 1000, 1)
        

        put_oi_list = []
        for i in range(len(df)):
            int_put_oi = int(df.iloc[i, [20]][0])
            put_oi_list.append(int_put_oi)
        put_oi_index = put_oi_list.index(max(put_oi_list))
        self.max_put_oi = round(max(put_oi_list) / 1000, 1)
        

        # total_call_oi = sum(call_oi_list)
        # total_put_oi = sum(put_oi_list)
        
        # try:
        #     self.put_call_ratio = round(total_put_oi / total_call_oi, 4)
        # except ZeroDivisionError:
        #     self.put_call_ratio = 0

        
        ## My logic for Volume difference

        call_vol_list = []
        for i in range(len(df)):
            int_call_vol = float(df.iloc[i, [2]][0])
            call_vol_list.append(int_call_vol)
        


        put_vol_list = []
        for i in range(len(df)):
            int_put_vol = float(df.iloc[i, [18]][0])
            put_vol_list.append(int_put_vol)
        


        total_call_vol = sum(call_vol_list)
        #print("Call vaol ",total_call_vol)
        total_put_vol = sum(put_vol_list)
        #print("put vaol ",total_put_vol)
       
        # #Highest 3 OI difference logic
        # df_max_OI= df['Change in Open Interest'].astype(float)
        # df_Call_max_OI = df_max_OI.iloc[:,0]
        # df_Put_max_OI = df_max_OI.iloc[:,1]
        
        # c3oi1,c3oi2,c3oi3 = df_Call_max_OI.nlargest(3,keep='last').index
        # p3oi1,p3oi2,p3oi3 = df_Put_max_OI.nlargest(3,keep='last').index

        # c3oi  = df.iloc[:, 1]
        # c3oi1_oi = c3oi.get((c3oi1), 'Change in Open Interest')
        # c3oi2_oi = c3oi.get((c3oi2), 'Change in Open Interest')
        # c3oi3_oi = c3oi.get((c3oi3), 'Change in Open Interest')
        # #print(c3oi1_oi,c3oi2_oi,c3oi3_oi)
        
        # #print(cvol1,cvol2,cvol3)
        # call_3oi = round(((c3oi1_oi+c3oi2_oi+c3oi3_oi) / 1000), 1)
        
        # p3oi  = df.iloc[:, 19]
        # p3oi1_oi = p3oi.get((p3oi1), 'Change in Open Interest')
        # p3oi2_oi = p3oi.get((p3oi2), 'Change in Open Interest')
        # p3oi3_oi = p3oi.get((p3oi3), 'Change in Open Interest')
        # #print(p3oi1_oi,p3oi2_oi,p3oi3_oi)
        # put_3oi = round(((p3oi1_oi+p3oi2_oi+p3oi3_oi) / 1000), 1)

               
        #print(total_put_vol)
        
        #max oi sp logic
        
        if self.first_run:
            self.MaxCStP = []
            self.MaxPStP = []

        self.MaxCStP = self.MaxCStP
        self.MaxPStP = self.MaxPStP
        
        self.max_call_oi_sp = df.iloc[call_oi_index]['Strike Price']
        self.MaxCStP.append(self.max_call_oi_sp)
        #print(self.MaxCStP)
        self.max_put_oi_sp = df.iloc[put_oi_index]['Strike Price']
        self.MaxPStP.append(self.max_put_oi_sp)
        #print(self.MaxPStP)
        if len(self.MaxCStP)>1:
            if self.MaxCStP[-2] != self.MaxCStP[-1]:
                messagebox.showinfo(title="Call OI Strick Price", message="The {} Call Max OI Strick Price is change from {} to {}".format(self.index,self.MaxCStP[-2], self.MaxCStP[-1]))
        if len(self.MaxPStP)>1:
            if self.MaxPStP[-2] != self.MaxPStP[-1]:
                messagebox.showinfo(title="Put OI Strick Price", message="The {} Put Max OI Strick Price is change from {} to {}".format(self.index,self.MaxPStP[-2], self.MaxPStP[-1]))
            
                
        
        
        #print("Spotprice",self.spotprice)


        try:
            index = int(df[df['Strike Price'] == self.sp].index.tolist()[0]) ## replace self.sp with self.spotprice to change the fix to dynamic slection of CHOI
        except IndexError as err:
            print(err, "10")
            messagebox.showerror(title="Error",
                                 message="Incorrect Strike Price.\nPlease enter correct Strike Price.")
            self.root.destroy()
            return
        
        
        ## IV cacluation 
        
        iv_dfC = df.iloc[:, 3]
        if self.first_run:
            self.civ_list = []
            self.piv_list = []
            self.tciv_list = []
            self.tpiv_list = []
            self.time_iv = []
        
        self.civ_list = self.civ_list
        self.piv_list = self.piv_list
        self.tciv_list = self.tciv_list
        self.tpiv_list = self.tpiv_list
        self.time_iv = self.time_iv
        for numi in range(5):
            civ_up = iv_dfC.get((index + numi), 'Implied Volatility')
            self.civ_list.append(civ_up)
        
        for numi in range(5):
            civ_down = iv_dfC.get((index - numi), 'Implied Volatility')
            self.civ_list.append(civ_down)

        if len(self.civ_list) <= 0:
            self.civ_list = self.civ_list + [0]
        else:
            civ_list_val = (sum(self.civ_list)/len(self.civ_list))
            self.tciv_list.append(civ_list_val)
            #print(self.tciv_list)
            
             
        iv_dfP = df.iloc[:, 17]
        
        for numi in range(5):
            piv_up = iv_dfP.get((index + numi), 'Implied Volatility')
            self.piv_list.append(piv_up)
        for numi in range(5):
            piv_down = iv_dfP.get((index - numi), 'Implied Volatility')
            self.piv_list.append(piv_down)
        
        if len(self.piv_list) <= 0:
            self.piv_list = self.piv_list + [0]
        else:
            piv_list_val = (sum(self.piv_list)/len(self.piv_list))
            self.tpiv_list.append(piv_list_val)
            #print(self.tpiv_list)
            
        self.time_iv.append(self.str_current_time)
        #print(self.time_iv)
        

        ## OI Logic
        OI_dfC = df.iloc[:, 0]
        self.cOI_list = []
        for numi in range(5):
            cOI_up = OI_dfC.get((index + numi), 'Open Interest')
            self.cOI_list.append(cOI_up)
        
        for numi in range(5):
            cOI_down = OI_dfC.get((index - numi), 'Open Interest')
            self.cOI_list.append(cOI_down)

        if len(self.cOI_list) <= 0:
            self.cOI_list = self.cOI_list + [0]
        else:
            self.cOI_list = [sum(self.cOI_list)]
        
        
        OI_dfP = df.iloc[:, 20]
        self.pOI_list = []
        for numi in range(5):
            pOI_up = OI_dfP.get((index + numi), 'Open Interest')
            self.pOI_list.append(pOI_up)
        for numi in range(5):
            pOI_down = OI_dfP.get((index - numi), 'Open Interest')
            self.pOI_list.append(pOI_down)
        
        if len(self.pOI_list) <= 0:
            self.pOI_list = self.pOI_list + [0]
        else:
            self.pOI_list = [sum(self.pOI_list)]
        
        totalOI = (sum(self.cOI_list) + sum(self.pOI_list))/1000 # reduse to k
        
        if self.first_run:
            self.totaOI = []
        self.totaOI = self.totaOI
        self.totaOI.append(totalOI)


        
        ## Change in OI logic
        a = df[['Change in Open Interest']][df['Strike Price'] == self.sp]
        b1 = a.iloc[:, 0]
        c1 = b1.get(index)
        #b2 = df.iloc[:, 1]
        c2 = 0
        b3 = df.iloc[:, 1]
        c3 = 0
        c3_list = []
        
        for numi in range(5):
            c33 = b3.get((index + numi), 'Change in Open Interest')
            c3_list.append(c33)
            
            
        for numi in range(5):
            c33 = b3.get((index - numi), 'Change in Open Interest')
            c3_list.append(c33)
            
        if isinstance(c2, str):
            c2 = 0
        if isinstance(c3, str):
            c3 = 0
         
        self.call_sum = round((sum(c3_list) / 1000), 1)
        #call_sum_oi = self.call_sum 
        
        # Logic for Open interest calculation call
        ## Ranjeet Logic
        df_oi3= df['Open Interest'].astype(float)
        df_Call_vol = df_oi3.iloc[:,0]
        df_Put_vol = df_oi3.iloc[:,1]
        
        cl1,cl2,cl3 = df_Call_vol.nlargest(3,keep='last').index
        pl1,pl2,pl3 = df_Put_vol.nlargest(3,keep='last').index
        
        
        

        #aa = df[['Change in Open Interest']][df['Strike Price'] == self.sp]
        bvol = df.iloc[:, 1]
        cvol1 = bvol.get((cl1), 'Change in Open Interest')
        cvol2 = bvol.get((cl2), 'Change in Open Interest')
        cvol3 = bvol.get((cl3), 'Change in Open Interest')
        #print(cvol1,cvol2,cvol3)
        self.call_boundary = round(((cvol1+cvol2+cvol3) / 1000), 1)
        

        
        if self.call_boundary == -0:
            self.call_boundary = 0.0
            
        # Logic for Change in OI Put
   
        #o1 = a.iloc[:, 1]
        #p1 = o1.get(index)
        o2 = df.iloc[:, 19]
        p2 = 0
        p3 = 0
        p3_list = []
        
        for numi in range(5):
            p33 = o2.get((index + numi), 'Change in Open Interest')
            p3_list.append(p33)
            
        for numi in range(5):
            p33 = o2.get((index - numi), 'Change in Open Interest')
            p3_list.append(p33)

            
        # self.p4 = o2.get((index + 4), 'Change in Open Interest')
        # o3 = df.iloc[:, 1]
        # self.p5 = o3.get((index + 4), 'Change in Open Interest')
        # self.p6 = o3.get((index - 2), 'Change in Open Interest')
        # self.p7 = o2.get((index - 2), 'Change in Open Interest')
        if isinstance(p2, str):
            p2 = 0
        if isinstance(p3, str):
            p3 = 0
        # if isinstance(self.p4, str):
        #     self.p4 = 0
        # if isinstance(self.p5, str):
        #     self.p5 = 0
        self.put_sum = round((sum(p3_list) / 1000), 1)
   
        
        
        #put_sum_oi = self.put_sum
        
        # Logic for Open intresrt Put
        pvol = df.iloc[:, 19]
        pvol1 = pvol.get((pl1), 'Change in Open Interest')
        pvol2 = pvol.get((pl2), 'Change in Open Interest')
        pvol3 = pvol.get((pl3), 'Change in Open Interest')
        #print(pvol1,pvol2,pvol3)


        
        self.put_boundary = round(((pvol1+pvol2+pvol3) / 1000), 1)
        
        # Calculations 
        call_boundary_oi = self.call_boundary
        put_boundary_oi = self.put_boundary
        if call_boundary_oi ==0:
            call_boundary_oi_pc = 0 
        else:
            call_boundary_oi_pc = (call_boundary_oi/(call_boundary_oi+put_boundary_oi))*100
        
        if put_boundary_oi == 0:
            put_boundary_oi_pc = 0
        else:
            put_boundary_oi_pc = (put_boundary_oi/(put_boundary_oi+call_boundary_oi))*100
        
        if self.put_boundary == 0:
            self.put_boundary = 0.0
        
        # Logic for only CHOI difference  
        self.difference = round(self.put_sum - self.call_sum, 2)
        
        if self.call_sum == 0 :
            self.put_call_ratio = 0
        else :
            self.put_call_ratio = (self.put_sum / self.call_sum)

       
            


        ## Second max OI logic change to IV (Implied Volatility & Option LTP)
            
        aaiv = df[['Implied Volatility']][df['Strike Price'] == self.spotprice]
        aaltp = df[['Last Traded Price']][df['Strike Price'] == self.spotprice]
        #print(aaiv)
        #print(aaltp)
        
        if aaiv.empty == False :
            call_sp_iv = (aaiv.iloc[0][0])
            call_sp_ltp = (aaltp.iloc[0][0])
            
            put_sp_iv = (aaiv.iloc[0][1])
            put_sp_ltp = (aaltp.iloc[0][1])
        else:
            call_sp_iv = 0
            call_sp_ltp = 0
            
            put_sp_iv = 0
            put_sp_ltp = 0
            
            
        #print(aaiv.iloc[0][0])
        #print(aaiv.iloc[0][1])
        # Call IV
        self.max_call_oi_2 = call_sp_iv
        # Call LTP
        self.max_call_oi_sp_2 = call_sp_ltp
        # Put IV
        self.max_put_oi_2 = put_sp_iv
        ## PUT LTP
        self.max_put_oi_sp_2 = put_sp_ltp

        
        ##
        # CHOI difference logic

        try:
            
            self.call_itm = round(put_boundary_oi_pc - call_boundary_oi_pc,2) 
            #print(put_boundary_oi )

        except ZeroDivisionError:
            self.call_itm = 0
        
        try:
            self.put_itm = round(((total_put_vol - total_call_vol)/10000 ), 1) # Volume diff
        except ZeroDivisionError:
            self.put_itm = 0

        
        if self.stop:
            return

        self.set_values()

        if self.first_run:
            self.first_run = False
        
        #print(type(self.points))
        self.root.after((self.seconds * 360), self.main)
        # Endtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(Endtime)
        return

    @staticmethod
    def create_instance():
        master_window = Tk()
        NseOI(master_window)
        master_window.mainloop()


if __name__ == '__main__':
    NseOI.create_instance()


