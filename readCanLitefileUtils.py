import numpy as np
import matplotlib
import statistics
import pandas as pd

def GetADCvalues(file_DACset):

    tmp_df = pd.read_csv(file_DACset)

    #remove some columns not exploitable
    tmp_df.drop(['Bus','No', 'ID (hex)', 'Message', 'ASCII'], inplace=True, axis=1)

    #save dataframe in a file to be read by the script
    filename = file_DACset.split('/')[2]
    tmp_filename = 'calibfile_fromscript_'+ filename+'.txt'
    tmp_df.to_csv(tmp_filename, sep=',', index=False, header=False, quotechar = ' ')

    #open file to read
    infile = open(tmp_filename, 'r')

    #call function which read the file and return the content ordered in a list of dictionaries
    d_list = readfile(infile)

    DAC_set = getDACsetperchannel(d_list)
    DAC_set

    my_allch_list = getADCperchannel(d_list)
    mych_average_biasV = Getch_average(my_allch_list)
    hexprint = list(map(trunchex, mych_average_biasV))

    HV = getHV(d_list)

    return DAC_set, hexprint, HV

# define a function which reads the file and return a list of dictionaries contaning all requests and answers organised 
# the final format of each list item is a dictionary with the following structure:
# {'timestamp': '4346.454.319.0',
#  'state': 'S',
#  'mssg_length': '2',
#  'mssg': '0101',
#  'answer': ['01  00  00  00  00  00  00', '21  00  00  00  00  00  00']},

def readfile(filein):
    Lines = filein.readlines()

    #definition of the dictionary with the possible requests which can be found and the expected length of the answers
    d_request = {'0101' : 2, '0102': 2, '0106': 4, '0105': 4, '0109': 2, '0100': 2, '0104': 4 }

    #define a global list of dictionary: this will be the object returned by the function
    my_d_list = []

    # loop over lines. The iterator i is needed to be able to extract the lines containing the answers
    for i in range(0, len(Lines)):
        line = Lines[i]
        
        #split line and get each element separately. Using ',' as separator
        singles = line.split(',') 

        #remove some whitespace from the State element to be more handy
        singles[1] = singles[1].strip()

        #build a tmp dictionary which will be then saved in the global list of dictionary d_list
        tmp_dic = {'timestamp':singles[0], 'state': singles[1], 'mssg_length':singles[2], 'mssg':singles[3] } 
        


        list(tmp_dic)
        if (tmp_dic.get('state')== 'S'):
            
            #remove some whitespace from the request element to be more handy
            message = tmp_dic.get('mssg').strip()
            message = message.replace(' ', '')

            #replace mssg in the dictionary
            tmp_dic.update(mssg=message)

            #print('this is a request:', tmp_dic.get('state'))
            #print('this is the message:', message)

            for value in d_request.keys():
                #print(value)
                if (message== value):
                    #get the answer length to know how many lines we have to read
                    answer_length = d_request.get(value)
            
                    #prepare a list to record the answer
                    aws =[] 

                    #loop over the line of the answer: 
                    for a_i in range(1, answer_length+1):
                        awsline = Lines[i+a_i].split(',') 
                        aws.append(awsline[3].strip())    
                        
                    #print('printing the answer: ', aws)
                    tmp_dic['answer'] = aws
                    my_d_list.append(tmp_dic)
                    #print('print dictionary list', d_list)
                    
                    
    return my_d_list


# define a function which for cases of 4lines answers, 
# returns a list of list recording the values per channel 

def ExtractCh_4linesansw(answ, list_ch):
    
    if (len(answ) !=4): abort

    for answ_items in answ:
        answ_items = answ_items.split(' ')
        
        if (answ_items[0] == '01'):
            list_ch[0].append(answ_items[2]+answ_items[4])
            list_ch[1].append(answ_items[6]+answ_items[8])
            list_ch[2].append(answ_items[10]+answ_items[12])

        elif (answ_items[0] == '21'):
            list_ch[3].append(answ_items[2]+answ_items[4])
            list_ch[4].append(answ_items[6]+answ_items[8])
            list_ch[5].append(answ_items[10]+answ_items[12])
        
        elif (answ_items[0] == '41'):
            list_ch[6].append(answ_items[2]+answ_items[4])
            list_ch[7].append(answ_items[6]+answ_items[8])
            list_ch[8].append(answ_items[10]+answ_items[12])

        elif (answ_items[0] == '61'):
            list_ch[9].append(answ_items[2]+answ_items[4])
            list_ch[10].append(answ_items[6]+answ_items[8])
            list_ch[11].append(answ_items[10]+answ_items[12])
    

    return list_ch





#define a function which take in input a list of dictionary and 
# search for the request 0105 (DACset) to define the setting point for the following measurements 

def getDACsetperchannel(mylist):
    for d in mylist:
        if (d.get('mssg')=='0104'):
            answ = d.get('answer')

            #create the dictionary which will collect all the channels infos
            l_ch0, l_ch1, l_ch2 = [], [], []
            l_ch3, l_ch4, l_ch5 = [], [], []
            l_ch6, l_ch7, l_ch8 = [], [], []
            l_ch9, l_ch10, l_ch11 = [], [], []

            # define the list of list which will contain all the list of single channels values recording their ADC values
            l_allch = []


            #add all channel to the list of list to return
            l_allch.extend([l_ch0,l_ch1,l_ch2,l_ch3, l_ch4, l_ch5, l_ch6, l_ch7, l_ch8, l_ch9, l_ch10, l_ch11])
    
            list_ch_dacset = ExtractCh_4linesansw(answ, l_allch)

            #print(list_ch_dacset)
            
            #print('now find which DACset we have: ')
            mych_average_dacset = Getch_average(list_ch_dacset)    

    areallthesame = all(x==mych_average_dacset[0] for x in mych_average_dacset)

    if (areallthesame == True ):
        DAC_set = mych_average_dacset[0]
    else:
        DAC_set = 9999

    return DAC_set


#define a function which take in input a list of dictionary and 
# search for the request 0105 and separate the channel

def getADCperchannel(mylist):

    mylist = mylist.copy()

    #create the dictionary which will collect all the channels infos
    l_ch0, l_ch1, l_ch2 = [], [], []
    l_ch3, l_ch4, l_ch5 = [], [], []
    l_ch6, l_ch7, l_ch8 = [], [], []
    l_ch9, l_ch10, l_ch11 = [], [], []

    # define the list of list which will contain all the list of single channels values recording their ADC values
    l_allch = []

    #add all channel to the list of list to return
    l_allch.extend([l_ch0,l_ch1,l_ch2,l_ch3, l_ch4, l_ch5, l_ch6, l_ch7, l_ch8, l_ch9, l_ch10, l_ch11])


    for d in mylist:
        if (d.get('mssg')=='0105'):
            answ = d.get('answer')

            l_allch = ExtractCh_4linesansw(answ, l_allch)

    #return the list of list
    return(l_allch)    


def GetHVvalue(myfile):

    tmp_df = pd.read_csv(myfile)

    #remove some columns not exploitable
    tmp_df.drop(['Bus','No', 'ID (hex)', 'Message', 'ASCII'], inplace=True, axis=1)

    #save dataframe in a file to be read by the script
    filename = myfile.split('/')[2]
    tmp_filename = 'HVcalibfile_fromscript_'+ filename+'.txt'
    tmp_df.to_csv(tmp_filename, sep=',', index=False, header=False, quotechar = ' ')

    #open file to read
    infile = open(tmp_filename, 'r')

    #call function which read the file and return the content ordered in a list of dictionaries
    d_list = readfile(infile)

    HV = getHV(d_list)
    return HV


def getHV(mylist):

    mylist = mylist.copy()

    list_HV = []

    for d in mylist:
        
        if (d.get('mssg')=='0100'):
            answ = d.get('answer')
            #print(answ)

            if (len(answ) !=2): abort

            for answ_items in answ:
                answ_items = answ_items.split(' ')

                if (answ_items[0] == '01'):
                    list_HV.append(answ_items[2]+answ_items[4])


    #print(list_HV)
    list_HV_dec = map(todec, list_HV )
    HV_avg = statistics.mean(list_HV_dec)
    HV_hex = tohex(HV_avg)


    return  HV_hex




#function to convert hex to decimal
def todec(n):
    return int(n, 16) 

#function to convert back to hex (after rounding to get to the closest integer)
def tohex(n):
    return hex(round(n))


#function to get the list of list of all values per channel. Per each channel do: 
# - convert to dec compute the average
# - compute the average
# - store the value in a list (this will contain one value per channel )
# - convert the values in the list to hex 
# - return the list containing all the averages per channel --> these are the values to be used for the calibration campaign
#   

def Getch_average(chlist):
    chlist = chlist.copy()
    
    #check the length of the list, if different from 12, abort
    if (len(chlist)!=12): abort
    #print(len(chlist))
    
    ch_avg_dec = []
    ch_avg_hex = []

    for ch in chlist:

        # convert any elements of the channel list to decimal
        singlech_dec = list(map(todec, ch))
        #print(singlech_dec)
        
        #compute the average
        ch_avg = statistics.mean(singlech_dec)
        ch_avg_dec.append(ch_avg)

        #print(list(singlech_dec))
        #print(singlech_avg)

    #print(ch_avg_dec)
    #convert back to hex and save to a list which will be our final output
    ch_avg_hex = list(map(tohex, ch_avg_dec))
    #print(ch_avg_hex)
    return ch_avg_hex


def printhex(myhex):
    print(myhex[2:])

def trunchex(myhex):
    return (myhex[2:])
    