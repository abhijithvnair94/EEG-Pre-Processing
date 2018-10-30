                                  """
Created on Mon Aug 20 14:59:48 2018

@author: Abhi
"""


#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from scipy import signal

###############################################################################################
'''Data Reading '''
data = pd.read_csv('/home/mtp-1/pro/codes/exp_3-familiarisation/EEG_raw_data/nikhil/nik_test_2_edit.csv')
#print(data.iloc[:,0].values())

p7 = data.iloc[:,0].values
p8 = data.iloc[:,1].values
o1 = data.iloc[:,2].values
o2 = data.iloc[:,3].values
# plt.plot(p7)
# plt.show()

# print(p7)
#############################################################################################
#'''Detrending of the data -- eliminating DC offset'''
def detrend(val):
    p7_1 = list()
    for i in range(1, len(val)):
        value = val[i] - val[i - 1]
        p7_1.append(value)
        
    return p7_1

p7 = detrend(p7)
p8 = detrend(p8)
o1 = detrend(o1)
o2 = detrend(o2)

time_sec = list()

for i in range(0,len(p7)):
    time_sec.append(i+1)

data['time in sec'] = pd.Series(time_sec)
data['P7'] = pd.Series(p7)
data['P8'] = pd.Series(p8)
data['O1'] = pd.Series(o1)
data['O2'] = pd.Series(o2)  

data = data.drop(data.index[-1])

#############################################################################################
'''Applying an HPF '''

def high_pass_filter(sub_data,cutoff):
    nyq = 0.5 * 256
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(2, normal_cutoff, btype='high', analog=False)
    hpf = signal.filtfilt(b, a, sub_data)
    return hpf

#############################################################################################
'''Applying the Notch Filtering '''

def notch_filter(hpf):
    fs = 256
    f0 = 60 #frequency to remove
    Q = 30 #quality factor
    
    w0 = f0/(fs/2) #Normalised frequency
    #Design the Notch filter
    b, a = signal.iirnotch(w0, Q)
    
    # Frequency response
    #w, h = signal.freqz(b, a)
    filtered_data = signal.lfilter(b, a, hpf)
    
    return filtered_data


#plt.plot(filtered_data[:,0])
#plt.xlim(0,100)
#plt.show()


###############################################################################################
'''Apply Band Pass Filter '''

def low_pass_filter(filtered_data,lower):
    nyq = 0.5 * 256
    low = lower / nyq
    #high = 50 / nyq
    b, a = signal.butter(2,low, btype='low') #Design of BPF 
    y = signal.lfilter(b,a,filtered_data)
    
    return y

#plt.plot(y)
#plt.xlim(0,100)
#plt.show()

#print(y)
###############################################################################################


new_value = []
electrodes = [p7,p8,o1,o2]
for i in range(len(electrodes)):
    e_hpf = high_pass_filter(electrodes[i],0.5)
    e_notch = notch_filter(e_hpf)
    e_high = high_pass_filter(electrodes[i],4)  #making a bwf of 4-13hz
    e_filt = low_pass_filter(e_high,13)
    
    new_value.append(e_filt)

#print(new_value)
p7_new = new_value[0]
p8_new = new_value[1]
o1_new = new_value[2]
o2_new = new_value[3]

time_sec = list()

for i in range(0,len(p7)):
    time_sec.append(i+1)

data['time in sec'] = pd.Series(time_sec)
data['P7'] = pd.Series(p7_new)
data['P8'] = pd.Series(p8_new)
data['O1'] = pd.Series(o1_new)
data['O2'] = pd.Series(o2_new)  


#######################################################
'''Adding condition for fam or non '''
#case = list()
#i=0
#while i <= len(p7):
#   case.append(0)  #######CHECK HERE#############################
#   i =i+1
   
#data['case'] = pd.Series(case)    
########################################################
'''Saving the final file as csv '''


data.to_csv('/home/mtp-1/pro/codes/exp_3-familiarisation/EEG_raw_data/nikhil/filtered/nikhil_test_1_filt_13.csv',sep=',',encoding='utf-8')

