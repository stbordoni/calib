import numpy as np
import pandas as pd
import math       



def hex_to_dec(df) :
    df = df.copy()
    df['ADCmin'] = df['ADCmin'].apply(lambda x: int(x,16) )
    df['ADCmax'] = df['ADCmax'].apply(lambda x: int(x,16) )
    return df 


def biasV_params(df):
    df = df.copy()

    a_coeff = 1.8409e-3
    b_coeff = 0
        
    df['Gain BiasV'] = (df['DMMmax'] - df['DMMmin']) / (df['ADCmax'] - df['ADCmin'] ) * 1/a_coeff
    df['offset BiasV'] = df['ADCmin'] - (df['DMMmin'] - b_coeff )/ (df['Gain BiasV'] * a_coeff )

    return df


def HV_params(df):
    df = df.copy()

    a_coeff = 1.8535e-3
    b_coeff = 0
        
    df['Gain HV'] = (df['DMMmax'] - df['DMMmin']) / (df['ADCmax'] - df['ADCmin'] ) * 1/a_coeff
    df['offset HV'] = df['ADCmin'] - (df['DMMmin'] - b_coeff )/ (df['Gain HV'] * a_coeff)

    return df


""" def compute_gain(df, calib ):
    df = df.copy()
    if (calib == 'HV'):
        a_coeff = 1.8535e-3
        df['Gain HV'] = (df['DMMmax'] - df['DMMmin']) / (df['ADCmax'] - df['ADCmin'] ) * 1/a_coeff

    elif (calib == 'biasV'):
         a_coeff = 1.8409e-3
         df['Gain BiasV'] = (df['DMMmax'] - df['DMMmin']) / (df['ADCmax'] - df['ADCmin'] ) * 1/a_coeff

    else:
        a_coeff = 99999. 
        print('Non valid calib type')
        abort()


    return df """

    
    
"""     def compute_offset(df, calib):
        df = df.copy()
        if (calib == 'HV'):
            a_coeff = 1.8535e-3
            b_coeff = 0
            df['offset HV'] = df['ADCmin'] - (df['DMMmin'] - b_coeff )/ (df['Gain HV'] * a_coeff)

        elif (calib == 'biasV'):
            a_coeff = 1.8409e-3
            b_coeff = 0
            df['offset BiasV'] = df['ADCmin'] - (df['DMMmin'] - b_coeff )/ (df['Gain BiasV'] * a_coeff)

        else:
            a_coeff = 99999. 
            b_coeff = 99999.
            print('Non valid calib type')
            abort()

        return df
 """

def convertADC(df ):
    df = df.copy()
    df['ADCmin_conv'] = df['ADCmin']* 1.8409e-3
    df['ADCmax_conv'] = df['ADCmax']* 1.8409e-3

    return df

def convertADC_BiasV(df ):
    df= df.copy()
    df['ADCmin_conv'] = 108.7677 + df['ADCmin']* 1.535e-3
    df['ADCmax_conv'] = 108.7677 + df['ADCmax']* 1.535e-3

    return df



def code_offsetandgain(df, calib):
    df = df.copy()

    if (calib == 'biasV'):
        df['Gain_Usig BiasV'] = df['Gain BiasV'].apply(lambda x: math.ceil((x* 32768)))
        df['Offset_Sig BiasV'] = df['offset BiasV'].apply(lambda x: round(x) ) 
    
    elif (calib == 'HV'):
        df['Gain_Usig HV'] = df['Gain HV'].apply(lambda x: math.ceil((x* 32768)))
        df['Offset_Sig HV'] = df['offset HV'].apply(lambda x: round(x) ) 

    else:
        print('calib not found, please put either BiasV or HV')
        abort()

    return df



#def get_USig_gain(df):
#    df = df.copy()
#    df['Gain_Usig HV'] = df['Gain HV'].apply(lambda x: math.ceil((x* 32768)))
#    df['Gain_Usig BiasV'] = df['Gain BiasV'].apply(lambda x: math.ceil((x* 32768)))

#    return df

#def get_Sig_offset(df):
#    df= df.copy()
#    df['Offset_Sig HV'] = df['offset HV'].apply(lambda x: round(x) ) 
#    df['Offset_Sig BiasV'] = df['offset BiasV'].apply(lambda x: round(x) ) 

#    return df


def tohextwocompl(val, nbits):
    return hex((val + (1 << nbits)) % (1<<nbits) ) 


def tohex_16bitsrange02(val):
    return hex((2* val /65536) ) 


def convert_to_exadec(df,calib):
    df = df.copy()
    if (calib == 'biasV'):
        df['Gain_Usig BiasV'] = df['Gain_Usig BiasV'].apply(lambda x : hex(x) )
        df['Offset_Sig BiasV'] = df['Offset_Sig BiasV'].apply(lambda x : tohextwocompl(x,15) )
    elif(calib=='HV'):
        df['Gain_Usig HV'] = df['Gain_Usig HV'].apply(lambda x : hex(x) )
        df['Offset_Sig HV'] = df['Offset_Sig HV'].apply(lambda x : tohextwocompl(x,15) )
    else:
        print('calib not found, please put either BiasV or HV')
        abort()

    return df


#def convert_to_exadec(df):
#    df = df.copy()

#    df['Gain_Usig BiasV'] = df['Gain_Usig BiasV'].apply(lambda x : hex(x) )
#    df['Gain_Usig HV'] = df['Gain_Usig HV'].apply(lambda x : hex(x) )

#    df['Offset_Sig BiasV'] = df['Offset_Sig BiasV'].apply(lambda x : tohextwocompl(x,16) )
#    df['Offset_Sig HV'] = df['Offset_Sig HV'].apply(lambda x : tohextwocompl(x,16) )


#    return df
    