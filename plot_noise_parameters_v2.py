#!/usr/bin/env python

#ipdb> import os; os._exit(1)

# call as: python noise_parameters.py file_in

# =======================================
# Version 0.4
# 12 April, 2019
# michael.taylor AT reading DOT ac DOT uk
# =======================================

import os  
import os.path  
import glob  
import optparse 
from  optparse import OptionParser  
import sys   
import numpy as np
import numpy.ma as ma  
import xarray
import datetime  
import pandas as pd 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# =======================================    

def plot_variables(file_in):

    ds = xarray.open_dataset(file_in)
    timestamp = ds['time']
    positions = ds['positions']
    coefs = ds['coefs']
    prts = ds['prts']
    bb_counts_c3 = ds['bb_counts_c3']
    bb_counts_c3_mean = ds['bb_counts_c3_mean'] 
    bb_counts_c3_std = ds['bb_counts_c3_std'] 
    bb_counts_c4 = ds['bb_counts_c4'] 
    bb_counts_c4_mean = ds['bb_counts_c4_mean'] 
    bb_counts_c4_std = ds['bb_counts_c4_std'] 
    bb_counts_c5 = ds['bb_counts_c5'] 
    bb_counts_c5_mean = ds['bb_counts_c5_mean'] 
    bb_counts_c5_std = ds['bb_counts_c5_std'] 

    space_counts_c3 = ds['space_counts_c3'] 
    space_counts_c3_mean = ds['space_counts_c3_mean'] 
    space_counts_c3_std = ds['space_counts_c3_std'] 
    space_counts_c4 = ds['space_counts_c4'] 
    space_counts_c4_mean = ds['space_counts_c4_mean'] 
    space_counts_c4_std = ds['space_counts_c4_std'] 
    space_counts_c5 = ds['space_counts_c5'] 
    space_counts_c5_mean = ds['space_counts_c5_mean'] 
    space_counts_c5_std = ds['space_counts_c5_std'] 

    coef_calib_c3 = ds['coef_calib_c3'] 
    coef_calib_c4 = ds['coef_calib_c4'] 
    coef_calib_c5 = ds['coef_calib_c5'] 

    prt_counts = ds['prt_counts'] 
#    prt_temp = ds['prt_temp'] 
    prt_temp = ds['temp_prt'] 
#    prt_temp_mean = ds['prt_temp_mean'] 

    radiance_c3_radiance_bb = ds['radiance_c3_radiance_bb'] 
    radiance_c4_radiance_bb = ds['radiance_c4_radiance_bb'] 
    radiance_c5_radiance_bb = ds['radiance_c5_radiance_bb'] 
    radiance_c3_gain = ds['radiance_c3_gain'] 
    radiance_c4_gain = ds['radiance_c4_gain'] 
    radiance_c5_gain = ds['radiance_c5_gain'] 
#    radiance_c3_radiance_space = ds['radiance_c3_radiance_space'] 
#    radiance_c4_radiance_space = ds['radiance_c4_radiance_space'] 
#    radiance_c5_radiance_space = ds['radiance_c5_radiance_space'] 
    radiance_c3_radiance_space = ds['radiance_c3_space'] 
    radiance_c4_radiance_space = ds['radiance_c4_space'] 
    radiance_c5_radiance_space = ds['radiance_c5_space'] 
#    radiance_c3_counts_space = ds['radiance_c3_counts_space'] 
#    radiance_c4_counts_space = ds['radiance_c4_counts_space'] 
#    radiance_c5_counts_space = ds['radiance_c5_counts_space'] 
    radiance_c3_counts_space = ds['radiance_c3_counts_sp'] 
    radiance_c4_counts_space = ds['radiance_c4_counts_sp'] 
    radiance_c5_counts_space = ds['radiance_c5_counts_sp'] 
    radiance_c3_counts_bb = ds['radiance_c3_counts_bb'] 
    radiance_c4_counts_bb = ds['radiance_c4_counts_bb'] 
    radiance_c5_counts_bb = ds['radiance_c5_counts_bb'] 

    ramp_c3 = ds['ramp_c3'] 
    ramp_c4 = ds['ramp_c4'] 
    ramp_c5 = ds['ramp_c5'] 

    temp_detector_radiator = ds['temp_detector_radiator'] 
    temp_detector_electronics = ds['temp_detector_electronics'] 
    temp_detector_cooler = ds['temp_detector_cooler'] 
    temp_detector_baseplate = ds['temp_detector_baseplate'] 
    temp_detector_motor = ds['temp_detector_motor'] 
    temp_detector_adconv = ds['temp_detector_adconv'] 
    temp_detector_patch = ds['temp_detector_patch'] 
    temp_detector_patch_extended = ds['temp_detector_patch_extended'] 
    
#    fig, ax  = plt.subplots()
#    ax.plot(timestamp, bb_counts_c3, '-', markersize=0.2)
#    ax.grid()
#    ax.set_title(r'$3.7\mu m$ channel')
#    ax.set_ylabel(r'bb_counts_c3: 1-10')
#    ax.set_xlabel('time')
#    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
#    fig.autofmt_xdate()
#    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
#    plt.savefig('bb_counts_c3.png')
#    plt.close()
        
#    fig, ax  = plt.subplots()
#    ax.plot(timestamp, bb_counts_c4, '-', markersize=0.2)
#    ax.grid()
#    ax.set_title(r'$11\mu m$ channel')
#    ax.set_ylabel(r'bb_counts_c4: 1-10')
#    ax.set_xlabel('time')
#    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
#    fig.autofmt_xdate()
#    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
#    plt.savefig('bb_counts_c4.png')
#    plt.close()
    
#    fig, ax  = plt.subplots()
#    ax.plot(timestamp, bb_counts_c5, '-', markersize=0.2)
#    ax.grid()
#    ax.set_title(r'$12\mu m$ channel')
#    ax.set_ylabel(r'bb_counts_c5: 1-10')
#    ax.set_xlabel('time')
#    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
#    fig.autofmt_xdate()
#    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
#    plt.savefig('bb_counts_c5.png')
#    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, bb_counts_c3_mean+bb_counts_c3_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, bb_counts_c3_mean-bb_counts_c3_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, bb_counts_c3_mean, 'r-', markersize=0.2, label='$\mu$')
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'bb_counts_c3: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('bb_counts_c3_mean_std.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, bb_counts_c4_mean+bb_counts_c4_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, bb_counts_c4_mean-bb_counts_c4_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, bb_counts_c4_mean, 'r-', markersize=0.2, label='$\mu$')
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'bb_counts_c4: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('bb_counts_c4_mean_std.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, bb_counts_c5_mean+bb_counts_c5_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, bb_counts_c5_mean-bb_counts_c5_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, bb_counts_c5_mean, 'r-', markersize=0.2, label='$\mu$')
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'bb_counts_c5: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('bb_counts_c5_mean_std.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, coef_calib_c3, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'coef_calib_c3')
    ax.set_xlabel('time')
    plt.legend([r'a_{0}','a_{1}','a_{2}'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('coef_calib_c3.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, coef_calib_c4, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'coef_calib_c4')
    ax.set_xlabel('time')
    plt.legend([r'a_{0}','a_{1}','a_{2}'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('coef_calib_c4.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, coef_calib_c5, '-', markersize=0.2, label=None)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'coef_calib_c5')
    ax.set_xlabel('time')
#    plt.legend([r'a_{0}','a_{1}','a_{2}'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('coef_calib_c5.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, prt_temp, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'PRT counts')
    ax.set_ylabel(r'counts')
    ax.set_xlabel('time')
    plt.legend(['PRT-1','PRT-2','PRT-3','PRT-4'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('prt_counts.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, prt_temp, '-', markersize=0.2)
#    ax.plot(timestamp, prt_temp.mean(), 'k--')
    ax.grid()
    ax.set_title(r'PRT temperatures')
    ax.set_ylabel(r'temperature [K]')
    ax.set_xlabel('time')
#    plt.legend([r'PRT-1','PRT-2','PRT-3','PRT-4','$\mu$'],loc='best')
    plt.legend([r'PRT-1','PRT-2','PRT-3','PRT-4'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('prt_temp_mean.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c3_radiance_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'radiance_c3_radiance_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c3_radiance_bb.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c4_radiance_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'radiance_c4_radiance_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c4_radiance_bb.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c5_radiance_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'radiance_c5_radiance_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c5_radiance_bb.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c3_gain, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'radiance_c3_gain')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c3_gain.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c4_gain, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'radiance_c4_gain')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c4_gain.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c5_gain, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'radiance_c5_gain')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c5_gain.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c3_radiance_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'radiance_c3_radiance_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c3_radiance_space.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c4_radiance_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'radiance_c4_radiance_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c4_radiance_space.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c5_radiance_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'radiance_c5_radiance_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c5_radiance_space.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c3_counts_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'radiance_c3_counts_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c3_counts_space.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c4_counts_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'radiance_c4_counts_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c4_counts_space.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c5_counts_space, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'radiance_c5_counts_space')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c5_counts_space.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c3_counts_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'radiance_c3_counts_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c3_counts_bb.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c4_counts_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'radiance_c4_counts_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c4_counts_bb.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, radiance_c5_counts_bb, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'radiance_c5_counts_bb')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('radiance_c5_counts_bb.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, ramp_c3, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'ramp_c3')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('ramp_c3.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, ramp_c4, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'ramp_c4')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('ramp_c4.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, ramp_c5, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'ramp_c5')
    ax.set_xlabel('time')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('ramp_c5.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c3, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch3: positions 1-10')
    ax.set_xlabel('time')
    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch3.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c4, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch4: positions 1-10')
    ax.set_xlabel('time')
    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch4.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c5, '-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch5: positions 1-10')
    ax.set_xlabel('time')
    plt.legend(['1','2','3','4','5','6','7','8','9','10'],loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch5.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c3_mean+space_counts_c3_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, space_counts_c3_mean-space_counts_c3_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, space_counts_c3_mean, 'r-', markersize=0.2)
    ax.grid()
    ax.set_title(r'$3.7\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch3: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch3_mean_std.png')
    plt.close()

    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c4_mean+space_counts_c4_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, space_counts_c4_mean-space_counts_c4_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, space_counts_c4_mean, 'r-', markersize=0.2, label='$\mu$')
    ax.grid()
    ax.set_title(r'$11\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch4: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch4_mean_std.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, space_counts_c5_mean+space_counts_c5_std, 'b-', markersize=0.2, label='$\pm\sigma$')
    ax.plot(timestamp, space_counts_c5_mean-space_counts_c5_std, 'b-', markersize=0.2, label=None)
    ax.plot(timestamp, space_counts_c5_mean, 'r-', markersize=0.2, label='$\mu$')
    ax.grid()
    ax.set_title(r'$12\mu m$ channel')
    ax.set_ylabel(r'space_counts_ch5: $\mu\pm\sigma$')
    ax.set_xlabel('time')
    plt.legend(loc='best')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('space_counts_ch5_mean_std.png')
    plt.close()
    
    fig, ax  = plt.subplots()
    ax.plot(timestamp, temp_detector_radiator, '-', markersize=0.2, label='radiator')
    ax.plot(timestamp, temp_detector_electronics, '-', markersize=0.2, label='electronics')
    ax.plot(timestamp, temp_detector_cooler, '-', markersize=0.2, label='cooler')
    ax.plot(timestamp, temp_detector_baseplate, '-', markersize=0.2, label='baseplate')
    ax.plot(timestamp, temp_detector_motor, '-', markersize=0.2, label='motor')
    ax.plot(timestamp, temp_detector_adconv, '-', markersize=0.2, label='adconv')
    ax.plot(timestamp, temp_detector_patch, '-', markersize=0.2, label='path')
    ax.plot(timestamp, temp_detector_patch_extended, '-', markersize=0.2, label='patch_extended')
    ax.grid()
    ax.set_ylabel(r'detector temperature [$K$]')
    ax.set_xlabel('time')
    plt.legend(loc='center right')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%H:%M')
    plt.savefig('temp_detector.png')
    plt.close()    

if __name__ == "__main__":

    parser = OptionParser("usage: %prog file_in")
    (options, args) = parser.parse_args()
    file_in = args[0]
    plot_variables(file_in)


