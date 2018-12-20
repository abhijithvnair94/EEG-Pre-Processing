# EEG-Pre-Processing

The code given can use for preprocessing of EEG signals.

## Steps
1.Data loading using pandas library (since data was in .csv format)
2.Detrending the Data --> inorder to remove the DC offset contained in the data beacuse of the measuring device.
3.Notch Filtering --> To remove the noise effect due to surrounding device - mainly in 50Hz or 60Hz.
4.Bandpass filtering --> Better to apply an High Pass Filter and then an Low Pass Filter instead of a single Band Pass Filtering.      
               that is more effective.
5.Save the file

### Note: 
    Its a simple preprocessing methods that can be used for EEG signals. I used only 4 electrodes O1,O2,P7 and P8 for project purpose. Also data can't be revealed now. Later I will. 
    
 Thank you!!!:)
