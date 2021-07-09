# calib
Few lines of codes to be improved and structured to perform the calibration of the SlowControl boards for the ToF detector for the ND280 upgrade

The code just read a csv file where the basic data with bias Voltage ON/OFF are recorded and perform the simple calculations to extract the offset and the gain 
and then estimate the hex value to be plugged in to calibrate the board produced with the CANLite software. 

Files: 
1) ToFSCB_ExtractADCCalibParameters.ipynb --> it take in input the multimiter data and the three files generated while preparing the calibration and compute:
- the Bias Voltage offset and gain for the 11 channels and the 
- the GHV offset and gain 

The code return 3 files (2 for the database, the third "_checks" to compare the offset and gain values among the 24 boards)

2) compareCalibParams.ipynb --> file to have a quick check over the offset and gain extracted for the BiasVoltage of the 11 channel. 
The code take as input one of the files produced at point 1) 
2 simple plots are drawn, just to see if there are major deviations. 
To DO: add a plot to look close to the area where all boards working properly seems to sit

3) calibvalidation.ipynb --> file to validate the calibration procedure and extract the error per each board channel. 
The code take in input the values from the multimeter and the 4 files of data recorded with the CANLite software.
 