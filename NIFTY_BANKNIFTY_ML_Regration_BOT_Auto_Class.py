# ML program for stock

class ML_Reg:
    def __int__(self):
        pass
    def ml_regration_auto():
        # Regration Level 1 type program
        print("\n")
        #Importing the libraries
        import numpy as np
        import pandas as pd
        import math
        from datetime import datetime,date
        import matplotlib.pyplot as plt
        from nsepy import get_history
        
        Starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #program data pull start time
        pdate = datetime.now().strftime("%d-%m-%Y")
        textdate = datetime.now().strftime("%d%m%Y")
        Pst = datetime.now().strftime("%H:%M")
        Day = datetime.now().strftime("%A")
        Daydate = datetime.now().strftime("%d")
        
        Ddn = datetime.now().strftime("%d")
        Dmn = datetime.now().strftime("%m")
        Dyn = datetime.now().strftime("%Y")
        
        dd = int(Ddn)
        dm = int(Dmn)
        dy = int(Dyn)
        
        ## Import from NSEpy python lab function
        nf50_History = get_history(symbol="NIFTY 50",start=date(2019,1,1),end=date(dy,dm,dd),index=True)
        bn_History = get_history(symbol="NIFTY BANK",start=date(2019,1,1),end=date(dy,dm,dd),index=True)
        #fin_History = get_history(symbol="NIFTY FIN SERVICE",start=date(2016,1,1),end=date(dy,dm,dd),index=True)
        
        ## For NIFTY 50 # Importing the dataset from csv file
        ## nfdataset = pd.read_csv('NIFTY_50_Data_2021.csv') #Csv file for offline
    
        nfdataset = nf50_History
        nfdataset['pdAvg'] = (nfdataset['Open']+nfdataset['High']+nfdataset['Low']+nfdataset['Close'])/4
        print("For Verification of data pull Nifty Yesterdays Close: ",nfdataset.iloc[len(nfdataset.index)-1][3])
        
        nfdataset['YClose'] = nfdataset['Close'].shift(1)
        nfdataset['pdAvg'] = nfdataset['pdAvg'].shift(2)
        nfx_o_h = nfdataset.iloc[2:, [0,1,7,6]].values    #values # Taking x as open and high & avrage of previous values & yclose value
        nfx_o_l = nfdataset.iloc[2:, [0,2,7,6]].values    #values # Taking x as open and Low & avrage of previous values & yclose value
        nfy_l = nfdataset.iloc[2:, 2].values # Taking y as low value
        nfy_h = nfdataset.iloc[2:, 1].values # Taking y as high value
        
        ## For BANKNIFTY # Importing the dataset from csv file.
        ##bndataset = pd.read_csv('BANKNIFTY_Data_2021.csv') # CSV file
        
        bndataset = bn_History
        bndataset['pdAvg'] = (bndataset['Open']+bndataset['High']+bndataset['Low']+bndataset['Close'])/4
        print("For Verification of data pull BankNifty Yesterdays Close: ",bndataset.iloc[len(bndataset.index)-1][3])
        bndataset['YClose'] = bndataset['Close'].shift(1)
        bndataset['pdAvg'] = bndataset['pdAvg'].shift(2)
        bnx_o_h = bndataset.iloc[2:, [0,1,7,6]].values # Taking x as open,high & avrage of previous values & yclose  value
        bnx_o_l = bndataset.iloc[2:, [0,2,7,6]].values # Taking x as open,Low & avrage of previous values &   yclose value
        bny_l = bndataset.iloc[2:, 2].values # Taking y as low value
        bny_h = bndataset.iloc[2:, 1].values # Taking y as high value
        print("\n")
        ## For test data use ##x_test1.reshape(3,1) if needed
        ## For Current values Importing the dataset from file nf_VIX_bn.csv from "in.investing.com"
        
        
        ## Manual process need to automated
        
        #COLUMN_NAMES = ['Name', 'Symbol', 'Last', 'Open', 'High', 'Low', 'Chg.', 'Chg. %','Vol.', 'Time']
        ML_file = 'ML_Watchlist_'+textdate+'.csv'
        
        cvdataset = pd.read_csv(ML_file) # read CSV file
        df_cvdataset1 = cvdataset.replace('\,','', regex=True)
        df_cvdataset = df_cvdataset1.replace('\%','', regex=True)
        df_cvdataset['Chg. %'].astype(float) # converting in to float
        df_cvdataset['Chg.'].astype(float) # converting in to float
        
        def nfcurrentvalue(CurrentLOC):
            CurrentValue = (float(df_cvdataset.iloc[CurrentLOC][2])+float(df_cvdataset.iloc[CurrentLOC][3])+float(df_cvdataset.iloc[CurrentLOC][4])+float(df_cvdataset.iloc[CurrentLOC][5]))/4
            return CurrentValue
        
        
        #Nifty 50
        nfltpv = float(df_cvdataset.iloc[13][2])
        nfov = float(df_cvdataset.iloc[13][3])
        nfhv = float(df_cvdataset.iloc[13][4])
        nflv = float(df_cvdataset.iloc[13][5])
        nfycv = float(nfdataset.iloc[-1][3])
        nfpdAvg = (nfov+nfhv+nflv+nfltpv)/4 
        
        """
        ##Old CSV file logic
        nf_VIX_bn_file = 'nf_VIX_bn_Watchlist_'+textdate+'.csv'
        cvdataset = pd.read_csv(nf_VIX_bn_file) # CSV file
        df_cvdataset1 = cvdataset.replace('\,','', regex=True)
        df_cvdataset = df_cvdataset1.replace('\%','', regex=True)
        """
        
        
        #VIX is use for VIX logic
        
        nfovix = float(df_cvdataset.iloc[14][3])
        nfhvix = float(df_cvdataset.iloc[14][4])
        nflvix = float(df_cvdataset.iloc[14][5])
        nfltpvix = float(df_cvdataset.iloc[14][2])
        nfpchangevix = float(df_cvdataset.iloc[14][7])  
        nfypcvix = float(df_cvdataset.iloc[14][2])
        
        #BankNifty
        bnltpv = float(df_cvdataset.iloc[12][2])
        bnov = float(df_cvdataset.iloc[12][3])
        bnhv = float(df_cvdataset.iloc[12][4])
        bnlv = float(df_cvdataset.iloc[12][5])
        bnycv = float(bndataset.iloc[-1][3])
        bnpdAvg = (bnov+bnhv+bnlv+bnltpv)/4 
        
        
        """
        # Manual entry
        print('For current values enter Nifty 50 & bankNifty Open, High , Low value & Yesterdays Close')
        
        current_values = [11539.45,11579.950,11520.70,11604.55,19.66,20.03,17.55,19.66,22352.35,22429.15,22292.35,22573.65] # Offline manual entry data 
        
        #Nifty
        nfov = float(current_values[0])
        nfhv = float(current_values[1])
        nflv = float(current_values[2])
        nfycv = float(current_values[3])
        nfovix = float(current_values[4])
        nfhvix = float(current_values[5])
        nflvix = float(current_values[6])
        nfypcvix = float(current_values[7])
        
        #BankNifty
        bnov = float(current_values[8])
        bnhv = float(current_values[9])
        bnlv = float(current_values[10])
        bnycv = float(current_values[11])
        """
            
        for mlploop  in range(4):
            if mlploop == 0: # taking ML values for predicting Nifty 50 Resistance
                x = nfx_o_l # input as low and open values
                y = nfy_h # output as high values act as Resistance
                ##offline current  data
                x_test1 = np.array([[nfov,nfhv,nfycv,nfpdAvg]]) 
            elif mlploop == 1:  # taking ML values for predicting Nifty 50 Support
                x = nfx_o_h # input as high and open values
                y = nfy_l # output as low values act as support
                ##offline current  data
                x_test1 = np.array([[nfov,nflv,nfycv,nfpdAvg]]) 
            elif mlploop == 2: # taking ML values for predicting Bank Nifty Resistance
                x = bnx_o_l # input as low and open values
                y = bny_h # output as high values act as Resistance
                ##offline current  data
                x_test1 = np.array([[bnov,bnhv,bnycv,bnpdAvg]])
            elif mlploop == 3:  # taking ML values for predicting Bank Nifty Support
                x = bnx_o_h # input as high and open values
                y = bny_l # output as low values act as support
                ##offline current  data
                x_test1 = np.array([[bnov,bnlv,bnycv,bnpdAvg]])
            
                
            # # # Splitting the dataset into the Training set and Test set ** if need to test accuresy 
            # from sklearn.model_selection  import train_test_split
            # x, x_test, y, y_test = train_test_split(x, y, test_size = 0.20, random_state = 10)
            
            
            ## Simple Linear Regression
            # Fitting Simple Linear Regression to the Training set
            from sklearn.linear_model import LinearRegression
            lr_regressor = LinearRegression()
            lr_regressor.fit(x, y)
            # Predicting the Test set results
            y_pred_lr = lr_regressor.predict(x_test1)
            #y_pred_lr = lr_regressor.predict(x_test)
            
            
            ##Polynomial Regression
            # Fitting Polynomial Regression to the dataset
            from sklearn.preprocessing import PolynomialFeatures
            poly_reg = PolynomialFeatures(degree = 4)
            x_poly = poly_reg.fit_transform(x)
            poly_reg.fit(x_poly, y)
            # New Fitting Linear Regression model to fit Polynomial Regression object
            pr_regressor = LinearRegression()
            pr_regressor.fit(x_poly, y)
            # Predicting the Test set results
            #y_pred_ploy = pr_regressor.predict(poly_reg.fit_transform(x_test))
            y_pred_ploy = pr_regressor.predict(poly_reg.fit_transform(x_test1))
            
            
            ## Decision Tree Regression
            # Fitting Decision Tree Regression to the dataset
            from sklearn.tree import DecisionTreeRegressor
            dtr_regressor = DecisionTreeRegressor(random_state = 0)
            dtr_regressor.fit(x, y)
            # Predicting a new result
            y_pred_dtr = dtr_regressor.predict(x_test1)
            #y_pred_dtr = dtr_regressor.predict(x_test)
            
            
            ## RandomFores Regressor Regression
            # Fitting RandomFores Regressor Regression to the dataset
            from sklearn.ensemble import RandomForestRegressor
            rf_regressor = RandomForestRegressor(n_estimators= 300,random_state = 0)
            rf_regressor.fit(x, y)
            # Predicting a new result
            y_pred_rf = rf_regressor.predict(x_test1)
            #y_pred_rf = rf_regressor.predict(x_test)
            
            ## Total prediction:
            y_predn = (y_pred_lr+y_pred_ploy+y_pred_dtr+y_pred_rf)/4
            y_pred = format(y_predn[0],'.2f')  #Converting array to string 
            #Print function
            #Append the Range in CSV file and write it to data frame
            if mlploop == 0:
                print('NIFTY 50  ML_Resistance {} '.format(y_pred))
                nf_y_pred_r = y_pred
                #print(('Nifty50_ML,{},{},{},{}'.format(pdate,'',nfov,y_pred)),file=open("Support_Resistance_data.csv", "a"))
            elif mlploop == 1:
                print('NIFTY 50  ML_Support    {} '.format(y_pred))
                print("\n")
                nf_y_pred_s = y_pred
                #print(('Nifty50_ML,{},{},{},{}'.format(pdate,y_pred,nfov,'')),file=open("Support_Resistance_data.csv", "a"))
            elif mlploop == 2:
                print('BANKNIFTY ML_Resistance  {} '.format(y_pred))
                bn_y_pred_r = y_pred
                #print(('BankNifty_ML,{},{},{},{}'.format(pdate,'',bnov,y_pred)),file=open("Support_Resistance_data.csv", "a"))
            elif mlploop == 3:
                print('BANKNIFTY ML_Support     {} '.format(y_pred))
                print("\n")
                bn_y_pred_s = y_pred
                #print(('BankNifty_ML,{},{},{},{}'.format(pdate,y_pred,bnov,'')),file=open("Support_Resistance_data.csv", "a"))
                
        
        
        
        # Calculate the Pchange with respect to yesterday close price
        nf_y_pred_r = float(nf_y_pred_r) # Conerting to float
        nf_y_pred_s = float(nf_y_pred_s)
        bn_y_pred_r = float(bn_y_pred_r)
        bn_y_pred_s = float(bn_y_pred_s)
        
        nfPChange_R_ML1 = ((nf_y_pred_r-nfycv)/nfycv)*100
        nfPChange_S_ML1 = ((nf_y_pred_s-nfycv)/nfycv)*100
        bnPChange_R_ML1 = ((bn_y_pred_r-bnycv)/bnycv)*100
        bnPChange_S_ML1 = ((bn_y_pred_s-bnycv)/bnycv)*100
        # Converting to print format
        nfPChange_R_ML = format(nfPChange_R_ML1,'.2f')
        nfPChange_S_ML = format(nfPChange_S_ML1,'.2f')
        bnPChange_R_ML = format(bnPChange_R_ML1,'.2f')
        bnPChange_S_ML = format(bnPChange_S_ML1,'.2f')
        
        print(('Nifty50_ML,{},{},{},{},{},{}'.format(pdate,nf_y_pred_s,nfov,nf_y_pred_r,nfPChange_S_ML,nfPChange_R_ML)),file=open("nf_Support_Resistance_data.csv", "a"))
        print(('BankNifty_ML,{},{},{},{},{},{}'.format(pdate,bn_y_pred_s,bnov,bn_y_pred_r,bnPChange_S_ML,bnPChange_R_ML)),file=open("bn_Support_Resistance_data.csv", "a"))
        

        
        # Taking close value of previous day
        nf_y_close =  nfdataset.iloc[-2][3]
        bn_y_close = bndataset.iloc[-2][3]
        
        # #Open High Low export for classification bot
        # print(('Nifty50_ML,{},{},{},{},{}'.format(pdate,nfov,nf_y_pred_r,nf_y_pred_s,nf_y_close)),file=open("nfClassification_input_data.csv", "a"))
        # print(('BankNifty_ML,{},{},{},{},{}'.format(pdate,bnov,bn_y_pred_r,bn_y_pred_s,bn_y_close)),file=open("bnClassification_input_data.csv", "a"))
        
        # #VIX Graph
        
        # print('VIX Graph')
        # nfLTP_PLOT = nfdataset.plot(x='Date',y='VIXClose')
        # plt.show()
        
        
        #For next month Aprox NIFTY 50 movment in persent:
        vixmpc = (float(nfltpvix)/3.465) 
        nmp = nfltpv+vixmpc
        nmn = nfltpv-vixmpc
        
        if float(nfpchangevix ) < 0.0 :
            ndpr = nfltpv-(float(nfltpvix) * float(nfpchangevix))
        else:
            ndpr = nfltpv+(float(nfltpvix) * float(nfpchangevix))
        
        
        if float(nfpchangevix ) > 0.0 :
            ndnr = nfltpv-(float(nfltpvix) * float(nfpchangevix))
        else:
            ndnr = nfltpv+(float(nfltpvix) * float(nfpchangevix))
        
        ndpf = format(ndpr,'.2f')
        ndnf = format(ndnr,'.2f')
        ndp = int(50 * round(float(ndpf)/50))
        ndn = int(50 * round(float(ndnf)/50))
        
        n50p = nfltpv
        
        nfPChange_R_ML1 = ((ndp-nfycv)/nfycv)*100
        nfPChange_S_ML1 = ((ndn-nfycv)/nfycv)*100
        # Converting to print format
        nfPChange_R_ML = format(nfPChange_R_ML1,'.2f')
        nfPChange_S_ML = format(nfPChange_S_ML1,'.2f')
        
        #Append the Range in CSV file and write it to data frame with Simple print fuction use for append value 
        print('Nifty_VIX,{},{},{},{},{},{}'.format(pdate,ndnf,n50p,ndpf,nfPChange_S_ML,nfPChange_R_ML),file=open("nf_Support_Resistance_data.csv", "a")) #Simple print fuction use for append value 
        print('Nifty 50 VIX_Resistance  {} \nNifty 50 VIX_Support     {}'.format(ndpf,ndnf)) 
        print("\n")
        
        if nfPChange_R_ML1>1.5 or bnPChange_R_ML1>1.5 or nfPChange_S_ML1< -1.5 or bnPChange_S_ML1<-1.5 :
            print("Best chance for option buying")    
    #Function call
    #ml_reg_auto = ml_regration_auto()
    
    
    def nf_bn_pcb():
        
        # PCB Price contribution base Level 0 type program

        #Importing the libraries
        import numpy as np
        import pandas as pd
        import math
        import csv
        from datetime import datetime
        
        
        Starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #program data pull start time
        Pst = datetime.now().strftime("%H:%M")
        Day = datetime.now().strftime("%A")
        Daydate = datetime.now().strftime("%d")
        pdate = datetime.now().strftime("%d-%m-%Y")
        textdate = datetime.now().strftime("%d%m%Y")
        
        
        ## For Current values Importing the dataset from file nf_VIX_bn.csv from "in.investing.com"
        ## Manual process need to automated
        
        #COLUMN_NAMES = ['Name', 'Symbol', 'Last', 'Open', 'High', 'Low', 'Chg.', 'Chg. %','Vol.', 'Time']
        ML_file = 'ML_Watchlist_'+textdate+'.csv'
        
        cvdataset = pd.read_csv(ML_file) # CSV file
        df_cvdataset1 = cvdataset.replace('\,','', regex=True)
        df_cvdataset = df_cvdataset1.replace('\%','', regex=True)
        df_cvdataset['Chg. %'] = df_cvdataset['Chg. %'].astype(float) # converting in to float
        df_cvdataset['Chg.'] = df_cvdataset['Chg.'].astype(float) # converting in to float
        df_cvdataset['High'] = df_cvdataset['High'].astype(float) 
        df_cvdataset['Low'] = df_cvdataset['Low'].astype(float)
        df_cvdataset['Open'] = df_cvdataset['Open'].astype(float) 
        df_cvdataset['hld'] = (df_cvdataset['High'] - df_cvdataset['Low']) 
        #df_cvdataset['hldp'] = (df_cvdataset['High'] - df_cvdataset['Low']) / ((df_cvdataset['High'] + df_cvdataset['Low'] +  df_cvdataset['Open'])/3) 
        
        #AXISBANK_value = float(df_cvdataset.iloc[0][2])+float(df_cvdataset.iloc[0][3])+float(df_cvdataset.iloc[0][4])+float(df_cvdataset.iloc[0][5])
        
        def bncurrentvalue(CurrentLOC):
            CurrentValue = (float(df_cvdataset.iloc[CurrentLOC][2])+float(df_cvdataset.iloc[CurrentLOC][3])+float(df_cvdataset.iloc[CurrentLOC][4])+float(df_cvdataset.iloc[CurrentLOC][5]))/4
            return CurrentValue
        
        AXISBANK_value = bncurrentvalue(0)
        Bandhan_value = bncurrentvalue(1)
        AUBANK_value = bncurrentvalue(2)
        Federal_value = bncurrentvalue(3)
        HDFCBANK_value = bncurrentvalue(4)
        ICICIBANK_value = bncurrentvalue(5)
        IDFC_value = bncurrentvalue(6)
        INDUSINDBK_value = bncurrentvalue(7)
        KOTAKBANK_value = bncurrentvalue(8)
        Punjab_value = bncurrentvalue(9)
        RBL_value = bncurrentvalue(10)
        SBIN_value = bncurrentvalue(11)
        
        RELIANCE_value = bncurrentvalue(18) 
        NF_HDFCBANK_value = bncurrentvalue(4)
        INFY_value = bncurrentvalue(19) 
        HDFC_value = bncurrentvalue(20) 
        NF_ICICIBANK_value = bncurrentvalue(5)
        TCS_value = bncurrentvalue(21)
        NF_KOTAKBANK_value = bncurrentvalue(8)
        HINDUNILVR_value = bncurrentvalue(22)
        ITC_value = bncurrentvalue(23)
        LT_value = bncurrentvalue(24)
        NF_AXISBANK_value = bncurrentvalue(0)
        BAJFINANCE_value = bncurrentvalue(25)
        ASIANPAINT_value = bncurrentvalue(26)
        BHARTIARTL_value = bncurrentvalue(27)
        NF_SBIN_value = bncurrentvalue(11)
        HCLTECH_value = bncurrentvalue(28)
        MARUTI_value = bncurrentvalue(29)
        MM_value = bncurrentvalue(30)
        NESTLEIND_value = bncurrentvalue(31)
        TITAN_value = bncurrentvalue(32)
        SUNPHARMA_value = bncurrentvalue(33)
        DRREDDY_value = bncurrentvalue(34)
        ULTRACEMCO_value = bncurrentvalue(35)
        TECHM_value = bncurrentvalue(36)
        WIPRO_value = bncurrentvalue(37)
        BAJAJFINSV_value = bncurrentvalue(38)
        HDFCLIFE_value = bncurrentvalue(39)
        NF_INDUSINDBK_value = bncurrentvalue(7)
        DIVISLAB_value = bncurrentvalue(40)
        POWERGRID_value = bncurrentvalue(41)
        NTPC_value = bncurrentvalue(42)
        TATASTEEL_value = bncurrentvalue(43)
        BAJAJ_AUTO_value = bncurrentvalue(44)
        BRITANNIA_value = bncurrentvalue(45)
        CIPLA_value = bncurrentvalue(46)
        HEROMOTOCO_value = bncurrentvalue(47)
        JSWSTEEL_value = bncurrentvalue(48)
        GRASIM_value = bncurrentvalue(49)
        ADANIPORTS_value = bncurrentvalue(50)
        EICHERMOT_value = bncurrentvalue(51)
        HINDALCO_value = bncurrentvalue(52)
        SBILIFE_value = bncurrentvalue(53)
        ONGC_value = bncurrentvalue(54)
        TATAMOTORS_value = bncurrentvalue(55)
        SHREECEM_value = bncurrentvalue(56) 
        BPCL_value = bncurrentvalue(57)
        COALINDIA_value = bncurrentvalue(58)
        UPL_value = bncurrentvalue(59)
        TATACONSUM_value = bncurrentvalue(60)
        IOC_value = bncurrentvalue(61)
        
        
        #Reading the CSV file for Lists
        #Add the PCB data point lists in csv file for future changes
        df_nf_bn_pcb = pd.read_csv('NF_BN_PCB_Lists.csv') # CSV file
        #nf_pcb_lst =[18,4,19,20,5,21,8,22,23,24,0,25,26,27,11,28,29,30,31,32,33,34,35,36,37,38,39,7,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61]
        nf_pcb_lst = df_nf_bn_pcb['nf_pcb_lst'].tolist()
        #Bank Nifty
        #stockPCtobn = [14.95,2.58,0.66,1.33,28.39,19.48,0.85,4.37,16.31,0.46,1.06,9.56] # Dec 2020 values
        
        #stockPCtobn = [16.59,2.11,1.0,1.46,26.89,20.01,1.0,4.85,13.55,0.67,0.97,10.93] # Feb 2021 values
        stockPCtobn = df_nf_bn_pcb['stockPCtobn'].tolist()
        
        # Calculated values stored as numbers
        stockValues = [AXISBANK_value,Bandhan_value,AUBANK_value,Federal_value,HDFCBANK_value,ICICIBANK_value,IDFC_value,INDUSINDBK_value,KOTAKBANK_value,Punjab_value,RBL_value,SBIN_value]
        
        #Avrage P change in stock = [AXISBANK_value = 3.00 ,Bandhan_value = 4.46 , AUBANK_value = 3.5,Federal_value = 3.43,HDFCBANK_value = 2.08 ,ICICIBANK_value =2.8 ,IDFC_value = 3.45,INDUSINDBK_value = 3.32,KOTAKBANK_value = 2.7 ,Punjab_value = 3.50,RBL_value = 4.01 ,SBIN_value=2.81]
        
        #bnST_PHLC = [3.00, 4.46 , 3.5 , 3.43 , 2.08 , 2.8 , 3.45 , 3.32 , 2.7 , 3.50 , 4.01 , 2.81 ] # Dec 2020 Values
        bnST_PHLC = df_nf_bn_pcb['bnST_PHLC'].tolist() 
  
        #BankNifty
        bnltpv = float(df_cvdataset.iloc[12][2])
        bnov = float(df_cvdataset.iloc[12][3])
        bnhv = float(df_cvdataset.iloc[12][4])
        bnlv = float(df_cvdataset.iloc[12][5])
        bnvalue = (bnltpv+bnov+bnhv+bnlv)/4
        bnaPHLC = 1.792
        bnpvalueby2d5 = float(df_cvdataset.iloc[12][10])/bnaPHLC
        bnpvaluemul2d5 = float(df_cvdataset.iloc[12][10])*bnaPHLC
        bnpvn = (bnvalue - bnpvalueby2d5)
        bnpvp = (bnvalue + bnpvaluemul2d5)
    
        #Nifty 50
        nfltpv = float(df_cvdataset.iloc[13][2])
        nfov = float(df_cvdataset.iloc[13][3])
        nfhv = float(df_cvdataset.iloc[13][4])
        nflv = float(df_cvdataset.iloc[13][5])
        nfvalue = (nfltpv+nfov+nfhv+nflv)/4
        nfaPHLC = 1.250
        nfpvalueby2d5 = float(df_cvdataset.iloc[13][10])/nfaPHLC
        nfpvaluemul2d5 = float(df_cvdataset.iloc[13][10])*nfaPHLC
        nfpvn = (nfvalue - nfpvalueby2d5)
        nfpvp = (nfvalue + nfpvaluemul2d5)
        
        ## calculated values for nifty 50 PCB 
        stockValuesNF = [RELIANCE_value,NF_HDFCBANK_value,INFY_value,HDFC_value,
                         NF_ICICIBANK_value,TCS_value,NF_KOTAKBANK_value,HINDUNILVR_value,
                         ITC_value,LT_value,NF_AXISBANK_value,BAJFINANCE_value,
                         ASIANPAINT_value,BHARTIARTL_value,NF_SBIN_value,HCLTECH_value,
                         MARUTI_value,MM_value,NESTLEIND_value,TITAN_value,
                         SUNPHARMA_value,DRREDDY_value,ULTRACEMCO_value,TECHM_value,
                         WIPRO_value,BAJAJFINSV_value,HDFCLIFE_value,NF_INDUSINDBK_value,
                         DIVISLAB_value,POWERGRID_value,NTPC_value,TATASTEEL_value,
                         BAJAJ_AUTO_value,BRITANNIA_value,CIPLA_value,HEROMOTOCO_value,
                         JSWSTEEL_value,GRASIM_value,ADANIPORTS_value,EICHERMOT_value,
                         HINDALCO_value,SBILIFE_value,ONGC_value,TATAMOTORS_value,
                         SHREECEM_value,BPCL_value,COALINDIA_value,UPL_value,
                         TATACONSUM_value,IOC_value]
        
        

        # stockPCtoNF = [10.73,10.45,7.7,7.61,6.11,4.98,4.84,3.54,
        #                3.02,2.57,2.55,2.32,2.06,2.03,1.75,1.7,
        #                1.68,1.14,1.09,1.08,1.06,1.05,1.01,1,
        #                0.95,0.89,0.88,0.84,0.81,0.81,0.8,0.8,
        #                0.74,0.7,0.69,0.67,0.62,0.6,0.59,0.58,
        #                0.58,0.58,0.56,0.55,0.53,0.51,0.47,0.42,
        #                0.38,0.38]
        
        stockPCtoNF = df_nf_bn_pcb['stockPCtoNF'].tolist() 
                            
        # nfST_PHLC = [2.358,2.091,2.174,2.457,2.81,2.303,2.693,2.224,
        #              2.279,2.523,3.013,3.516,2.48,3.166,2.823,2.73,
        #              2.54,2.83,2.414,3.154,2.858,2.465,2.718,2.958,
        #              2.496,3.408,3.07,3.336,2.904,2.386,2.528,3.165,
        #              2.553,2.746,2.602,2.655,3.559,2.727,3.578,3.294,
        #              3.613,3.037,2.871,3.356,3.309,3.259,2.682,3.489,
        #              3.015,2.991]
        
        nfST_PHLC = df_nf_bn_pcb['nfST_PHLC'].tolist() 

         
        

        def pvaluesfun_bn ():
            pvnList = []
            pvpList = []
            pvbnvalue = []
            for mulVal in range(12):
                pvalueby2d5 = float(df_cvdataset.iloc[mulVal][10])/bnST_PHLC[mulVal]
                pvaluemul2d5 = float(df_cvdataset.iloc[mulVal][10])*bnST_PHLC[mulVal]
                pvn = (stockValues[mulVal] - pvalueby2d5)*(stockPCtobn[mulVal]/100)
                pvp = (stockValues[mulVal] + pvaluemul2d5)*(stockPCtobn[mulVal]/100)
    
                pvnList.append(pvn) 
                pvpList.append(pvp)
                
            pvnListm = bnvalue-(bnvalue*(((sum(pvnList)/1000))/100))
            pvpListm = bnvalue+(bnvalue*(((sum(pvpList)/1000))/100))
            pvbnvalue.append(pvnListm)
            pvbnvalue.append(pvpListm)
            return pvbnvalue
        
        
        bn_pvalueList = pvaluesfun_bn()
        
        
        def pvaluesfun_nf():
            nfpvnList = []
            nfpvpList = []
            pvnfvalue = []
            for mulVal,lenVal in zip(nf_pcb_lst,range(len(nf_pcb_lst))):
                pvalueby2d5 = float(df_cvdataset.iloc[mulVal][10])/nfST_PHLC[lenVal]
                pvaluemul2d5 = float(df_cvdataset.iloc[mulVal][10])*nfST_PHLC[lenVal]
                pvn = (stockValuesNF[lenVal] - pvalueby2d5)*(stockPCtoNF[lenVal]/100)
                pvp = (stockValuesNF[lenVal] + pvaluemul2d5)*(stockPCtoNF[lenVal]/100)
    
                nfpvnList.append(pvn) 
                nfpvpList.append(pvp)
                
            nfpvnListm = nfvalue-(nfvalue*(((sum(nfpvnList)/1000))/100))
            nfpvpListm = nfvalue+(nfvalue*(((sum(nfpvpList)/1000))/100))
            pvnfvalue.append(nfpvnListm)
            pvnfvalue.append(nfpvpListm)
            return pvnfvalue
        nf_pvalueList = pvaluesfun_nf()
        
        
        #US Bank sector
        nqbank = float(df_cvdataset.iloc[16][7])
        djbank = float(df_cvdataset.iloc[17][7])
        
        
        def dfno(num):
            point = 0
            if (df_cvdataset.iloc[num][7]) > 0 and (df_cvdataset.iloc[num][7]) < 0.5:
                point = point + 1
            elif (df_cvdataset.iloc[num][7]) > 0.5 and (df_cvdataset.iloc[num][7]) < 1:
                point = point + 2
            elif (df_cvdataset.iloc[num][7]) > 1 :
                point = point + 3
            elif (df_cvdataset.iloc[num][7]) < 0 and (df_cvdataset.iloc[num][7]) > -0.5:
                point = point -1
            elif (df_cvdataset.iloc[num][7]) < -0.5 and (df_cvdataset.iloc[num][7]) > -1:
                point = point -2
            elif (df_cvdataset.iloc[num][7]) < -1 :
                point = point -3
            return point
        
        nqbank_p = dfno(16)
        djbank_p = dfno(17)
        points = (nqbank_p + djbank_p )/2
        
        if (points) >= 0 and (points) < 0.5:
            #print('Sideways US Bank')
            pt = 'Sideways US Bank'
        elif (points) >= 0.5 and (points) < 1:
            #print('Up and Positive US Bank')
            pt = 'Up and Positive US Bank'
        elif (points) >= 1 :
            #print('Strong Buy / Buy CE')
            pt = 'Strong Buy / Buy CE'
        elif (points) <= 0 and (points) > -0.5:
            #print('Sideways US Bank')
            pt = 'Sideways US Bank'
        elif (points) <= -0.5 and (points) > -1:
            #print('Down and Negative US Bank')
            pt= 'Down and Negative US Bank'
        elif (points) <= -1 :
            #print('Strong Sell / Buy PE')
            pt = 'Strong Sell / Buy PE'
        
        
        
        print("\n")
        print("For Todays BankNifty PCB Range at support {} and Resistance {}".format(format(bn_pvalueList[0],'.2f'),format(bn_pvalueList[1],'.2f')))
        print("\n")
        print("For Todays BankNifty Avrage Range  at low {} and at   High  {}".format(format(bnpvn,'.2f'),format(bnpvp,'.2f')))
        print("\n")
        print("For Todays US Bank are {} ".format(pt))
        print(('BankNifty_PCB,{},{},{},{},{},{}'.format(pdate,format(bn_pvalueList[0],'.2f'),bnvalue,format(bn_pvalueList[1],'.2f'),0,0)),file=open("BN_Support_Resistance_data.csv", "a"))
        print(('BankNifty_Avg.Range,{},{},{},{},{},{}'.format(pdate,format(bnpvn,'.2f'),bnvalue,format(bnpvp,'.2f'),0,0)),file=open("BN_Support_Resistance_data.csv", "a"))
        print("\n")
        print("For Todays Nifty50 PCB Range at support {} and Resistance {}".format(format(nf_pvalueList[0],'.2f'),format(nf_pvalueList[1],'.2f')))
        print("\n")
        print("For Todays Nifty50 Avrage Range  at low {} and at   High  {}".format(format(nfpvn,'.2f'),format(nfpvp,'.2f')))
        print("\n")
        print(('Nifty50_PCB,{},{},{},{},{},{}'.format(pdate,format(nf_pvalueList[0],'.2f'),nfvalue,format(nf_pvalueList[1],'.2f'),0,0)),file=open("NF_Support_Resistance_data.csv", "a"))
        print(('Nifty50_Avg.Range,{},{},{},{},{},{}'.format(pdate,format(nfpvn,'.2f'),nfvalue,format(nfpvp,'.2f'),0,0)),file=open("NF_Support_Resistance_data.csv", "a"))
        print("\n")
        ## ADR program to be added
        
        
    #Function call    
    #nf50_bn_pcb= nf_bn_pcb()

if __name__ == '__main__':
    ML_Reg()