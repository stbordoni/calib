# calib
Few lines of codes to be improved and structured to perform the calibration of the SlowControl boards for the ToF detector for the ND280 upgrade

The code just read a csv file where the basic data with bias Voltage ON/OFF are recorded and perform the simple calculations to extract the offset and the gain 
and then estimate the hex value to be plugged in to calibrate the board. 

ToDo: 
1) file with the common function to do the basic operations such a way for each card it will be just matter of calling those functions
2) small script which read a csv file and perform the basic operation calling the functions defined in the previous point
3) small script which read a generic csv file searching for the commands related to the calibration steps. After reading the file a cleaned cvs file with only 
the information relevant to the calibration should remain --> ready to call point 2)
