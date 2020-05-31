#!/usr/bin/env python

#ipdb> import os; os._exit(1)

# call as: python noise_parameters.py launchcode, year

# =======================================
# Version 0.9
# 2 April, 2019
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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# =======================================

def set_path_in(launchcode,year):
    """ 
    # ----------------------------------------------------
    # SET INPUT DIRECTORY FOR ASCII DATA FROM ELASTIC TAPE
    # ----------------------------------------------------
    """
    path = "/gws/nopw/j04/fiduceo/et_retrievals/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_ss_filtre/"
    path_in = os.path.join(path,"values_"+launchcode+"/"+year+"/")
    return path_in

def set_path_out(launchcode,year):
    """ 
    # ------------------------------------------
    # SET OUTPUT DIRECTORY FOR COMPRESSED NETCDF
    # ------------------------------------------
    """
    path = "/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper/"
    path_out = os.path.join(path,"values_"+launchcode+"/"+year+"/")
    path_out = path
    return path_out

def generate_orbit_list(launchcode,year,path_in,path_out):
    """ 
    # --------------------------------------------------------------
    # PARSE /SENSOR/YEAR DIRECTORY STRUCTURE AND GENERATE ORBIT LIST
    # --------------------------------------------------------------
    """
    orbit_list = os.path.join(path_out,launchcode + "_" + year + '.txt')
    os.system(f'\\ls -1f {path_in:s} > {orbit_list:s}')
    return orbit_list

def parse_orbit_list(orbit_list):
    """ 
    # ------------------------------------------------
    # PARSE ORBIT LIST AND CREATE VECTOR OF FILE NAMES
    # ------------------------------------------------
    """
    ds =  np.genfromtxt(orbit_list,dtype='str', skip_header=2)
    filevec = []
    for i in range(len(ds)):
        stub = "NM" + "_" + ds[i][-17:]
        if i == 0:
            filevec = np.append(filevec,stub)
        else:
            if not stub in filevec:
                filevec = np.append(filevec,stub)
    return filevec

def fix_datetime(path_in,file_in):
    """ 
    # -----------------------------------------------
    # LOAD + FIX INCORRECT DATETIMES IN MARINE'S DATA
    # -----------------------------------------------
    input file format: 
    year | month | day | day_numero | hours | utc_msecs | time 
    """
    filename = os.path.join(path_in,"date_"+file_in)
    ds = np.loadtxt(filename, skiprows=1)
    gd = ds[:,0] > 0
    for i in range(0,np.size(ds,axis=1)):
        if i==0:
            data = ds[gd,i][...,None]
        else:
            data = np.concatenate((data,ds[gd,i][...,None]),1)
    timestamp = []
    for i in range(len(data[:,0])):           
        datestr = str('{0:02d}'.format(data[i,0].astype('int64'))) + '-' + str('{0:02d}'.format(data[i,1].astype('int64'))) + '-' + str('{0:02d}'.format(data[i,2].astype('int64')))
        t_h = pd.to_datetime(data[i,4], unit='h') - pd.to_datetime('1970-01-01')
        t = pd.to_datetime(datestr) + t_h
        time = np.datetime64(t)
        epoch = np.datetime64('1970-01-01')
        t_s = np.array( (time-epoch), dtype='m8[s]').astype('float')
        timestamp = np.append(timestamp,t_s)
    timestamp = pd.to_datetime(timestamp, unit='s')
    return (timestamp, gd)

def mask_variables_time(timestamp,gd,path_in,file_in):
    """ 
    # --------------------------------------------
    # LOAD DATAFILES AND STORE VARIABLE TIMESERIES
    # --------------------------------------------
    """
    # bb_counts_1-10 | mean_bb_counts | stdev

    filename = os.path.join(path_in,"bb_counts_c3_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    bb_counts_c3 = data[gd,0:10]
    bb_counts_c3_mean = data[gd,10]
    bb_counts_c3_std = data[gd,11]
    filename = os.path.join(path_in,"bb_counts_c4_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    bb_counts_c4 = data[gd,0:10]
    bb_counts_c4_mean = data[gd,10]
    bb_counts_c4_std = data[gd,11]
    filename = os.path.join(path_in,"bb_counts_c5_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    bb_counts_c5 = data[gd,0:10]
    bb_counts_c5_mean = data[gd,10]
    bb_counts_c5_std = data[gd,11]

    # space_counts_1-10 | mean_space_counts | stdev

    filename = os.path.join(path_in,"space_counts_c3_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    space_counts_c3 = data[gd,0:10]
    space_counts_c3_mean = data[gd,10]
    space_counts_c3_std = data[gd,11]
    filename = os.path.join(path_in,"space_counts_c4_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    space_counts_c4 = data[gd,0:10]
    space_counts_c4_mean = data[gd,10]
    space_counts_c4_std = data[gd,11]
    filename = os.path.join(path_in,"space_counts_c5_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    space_counts_c5 = data[gd,0:10]
    space_counts_c5_mean = data[gd,10]
    space_counts_c5_std = data[gd,11]

    # radiance_bb | gain | Radiance_space | Space_view_counts | BB_view_counts

    filename = os.path.join(path_in,"radiance_c3_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    radiance_c3_radiance_bb = data[gd,0]
    radiance_c3_gain = data[gd,1]
    radiance_c3_radiance_space = data[gd,2]
    radiance_c3_counts_space = data[gd,3]
    radiance_c3_counts_bb = data[gd,4]
    filename = os.path.join(path_in,"radiance_c4_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    radiance_c4_radiance_bb = data[gd,0]
    radiance_c4_gain = data[gd,1]
    radiance_c4_radiance_space = data[gd,2]
    radiance_c4_counts_space = data[gd,3]
    radiance_c4_counts_bb = data[gd,4]
    filename = os.path.join(path_in,"radiance_c5_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    radiance_c5_radiance_bb = data[gd,0]
    radiance_c5_gain = data[gd,1]
    radiance_c5_radiance_space = data[gd,2]
    radiance_c5_counts_space = data[gd,3]
    radiance_c5_counts_bb = data[gd,4]

    # ramp: no header

    filename = os.path.join(path_in,"ramp_c3_"+file_in)
    data = np.loadtxt(filename, skiprows=0)
    ramp_c3 = data[gd]
    filename = os.path.join(path_in,"ramp_c4_"+file_in)
    data = np.loadtxt(filename, skiprows=0)
    ramp_c4 = data[gd]
    filename = os.path.join(path_in,"ramp_c5_"+file_in)
    data = np.loadtxt(filename, skiprows=0)
    ramp_c5 = data[gd]

    # detector: radiator | electronics(scanLinePos) | cooler | baseplate | motor | a_d_conv | patch | patchExtended

    filename = os.path.join(path_in,"temp_detector_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    temp_detector_radiator = data[gd,0]
    temp_detector_electronics = data[gd,1]
    temp_detector_cooler = data[gd,2]
    temp_detector_baseplate = data[gd,3]
    temp_detector_motor = data[gd,4]
    temp_detector_adconv = data[gd,5]
    temp_detector_patch = data[gd,6]
    temp_detector_patch_extended = data[gd,7]

    # coef_calib

    filename = os.path.join(path_in,"coef_calib_c3_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    coef_calib_c3 = data[gd,0:]
    filename = os.path.join(path_in,"coef_calib_c4_"+file_in)
    data = np.loadtxt(filename, skiprows=0)
    coef_calib_c4 = data[gd,0:]
    filename = os.path.join(path_in,"coef_calib_c5_"+file_in)
    data = np.loadtxt(filename, skiprows=0)
    coef_calib_c5 = data[gd,0:]

    # PRT_counts_1-4

    filename = os.path.join(path_in,"prt_counts_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    prt_counts = data[gd,0:]

    # PRT_temp_1-4 | mean

    filename = os.path.join(path_in,"temp_prt_"+file_in)
    data = np.loadtxt(filename, skiprows=1)
    prt_temp = data[gd,0:4]
    prt_temp_mean = data[gd,4]

    variables = {\
        0:bb_counts_c3, 1:bb_counts_c4, 2:bb_counts_c5,\
        3:bb_counts_c3_mean, 4:bb_counts_c4_mean, 5:bb_counts_c5_mean,\
        6:bb_counts_c3_std, 7:bb_counts_c4_std, 8:bb_counts_c5_std,\
        9:space_counts_c3, 10:space_counts_c4, 11:space_counts_c5,\
        12:space_counts_c3_mean, 13:space_counts_c4_mean, 14:space_counts_c5_mean,\
        15:space_counts_c3_std, 16:space_counts_c4_std, 17:space_counts_c5_std,\
        18:radiance_c3_radiance_bb, 19:radiance_c4_radiance_bb, 20:radiance_c5_radiance_bb,\
        21:radiance_c3_gain, 22:radiance_c4_gain, 23:radiance_c5_gain,\
        24:radiance_c3_radiance_space, 25:radiance_c4_radiance_space, 26:radiance_c5_radiance_space,\
        27:radiance_c3_counts_space, 28:radiance_c4_counts_space, 29:radiance_c5_counts_space,\
        30:radiance_c3_counts_bb, 31:radiance_c4_counts_bb, 32:radiance_c5_counts_bb,\
        33:ramp_c3, 34:ramp_c4, 35:ramp_c5,\
        36:temp_detector_radiator, 37:temp_detector_electronics, 38:temp_detector_cooler,\
        39:temp_detector_baseplate, 40:temp_detector_motor, 41:temp_detector_adconv,\
        42:temp_detector_patch, 43:temp_detector_patch_extended,\
        44:coef_calib_c3, 45:coef_calib_c4, 46:coef_calib_c5,\
        47:prt_counts, 48:prt_temp, 49:prt_temp_mean}

    return variables

def mask_variables_nan(timesetamp,variables):
    """ 
    # -----------------------------------
    # MASK MISSING VARIABLE DATA WITH NAN
    # -----------------------------------
    """
    for i in range(len(variables)):
        data = []
        if np.ndim(variables[i])>1:
            for j in range(np.shape(variables[i])[1]):
                var = variables[i][:,j]
                bd = ((var == -1.00000002E+30) | (var == -32768.0) | (var == -np.inf) | (var == 0.))
                var[bd] = np.NaN
                if j==0:
                    data = var[...,None]
                else:
                    data = np.concatenate((data,var[...,None]),1)
        else:
            var = variables[i][:]
            bd = ((var == -1.00000002E+30) | (var == -32768.0) | (var == -np.inf) | (var == 0.))
            var[bd] = np.NaN
            data = var[...,None]
            
        if i == 0:
            bb_counts_c3 = data
        elif i == 1:
            bb_counts_c4 = data
        elif i == 2:
            bb_counts_c5 = data
        elif i == 3:
            bb_counts_c3_mean = data
        elif i == 4:
            bb_counts_c4_mean = data
        elif i == 5:
            bb_counts_c5_mean = data
        elif i == 6:
            bb_counts_c3_std = data
        elif i == 7:
            bb_counts_c4_std = data
        elif i == 8:
            bb_counts_c5_std = data
        elif i == 9:
            space_counts_c3 = data
        elif i == 10:
            space_counts_c4 = data
        elif i == 11:
            space_counts_c5 = data
        elif i == 12:
            space_counts_c3_mean = data
        elif i == 13:
            space_counts_c4_mean = data
        elif i == 14:
            space_counts_c5_mean = data
        elif i == 15:
            space_counts_c3_std = data
        elif i == 16:
            space_counts_c4_std = data
        elif i == 17:
            space_counts_c5_std = data
        elif i == 18:
            radiance_c3_radiance_bb = data
        elif i == 19:
            radiance_c4_radiance_bb = data
        elif i == 20:
            radiance_c5_radiance_bb = data
        elif i == 21:
            radiance_c3_gain = data
        elif i == 22:
            radiance_c4_gain = data
        elif i == 23:
            radiance_c5_gain = data
        elif i == 24:
            radiance_c3_radiance_space = data
        elif i == 25:
            radiance_c4_radiance_space = data
        elif i == 26:
            radiance_c5_radiance_space = data
        elif i == 27:
            radiance_c3_counts_space = data
        elif i == 28:
            radiance_c4_counts_space = data
        elif i == 29:
            radiance_c5_counts_space = data
        elif i == 30:
            radiance_c3_counts_bb = data
        elif i == 31:
            radiance_c4_counts_bb = data
        elif i == 32:
            radiance_c5_counts_bb = data
        elif i == 33:
            ramp_c3 = data
        elif i == 34:
            ramp_c4 = data
        elif i == 35:
            ramp_c5 = data
        elif i == 36:
            temp_detector_radiator = data
        elif i == 37:
            temp_detector_electronics = data
        elif i == 38:
            temp_detector_cooler = data
        elif i == 39:
            temp_detector_baseplate = data
        elif i == 40:
            temp_detector_motor = data
        elif i == 41:
            temp_detector_adconv = data
        elif i == 42:
            temp_detector_patch = data
        elif i == 43:
            temp_detector_patch_extended = data
        elif i == 44:
            coef_calib_c3 = data
        elif i == 45:
            coef_calib_c4 = data
        elif i == 46:
            coef_calib_c5 = data
        elif i == 47:
            prt_counts = data
        elif i == 48:
            prt_temp = data
        elif i == 49:
            prt_temp_mean = data

    # -----------------------------------------------
    # PLOT VARIABLES (include code)
    # -----------------------------------------------

#    exec(open('plot_noise_parameters.py').read())

    # -----------------------------------------------
    # STORE AS XARRAY FOR WRITING TO NETCDF
    # -----------------------------------------------

    data_out = xarray.Dataset({"time": (("time",), np.atleast_1d(timestamp))})   
    data_out["time"].encoding['units'] = "seconds since 1970-1-1 00:00:00"
    data_out["positions"] = (("positions",), np.arange(0,10))
    data_out["coefs"] = (("coefs",), np.arange(0,3))
    data_out["prts"] = (("prts",), np.arange(0,4))
    data_out["bb_counts_c3"] = (("time","positions"), np.atleast_2d(bb_counts_c3))
    data_out["bb_counts_c4"] = (("time","positions"), np.atleast_2d(bb_counts_c4))
    data_out["bb_counts_c5"] = (("time","positions"), np.atleast_2d(bb_counts_c5))
    data_out["bb_counts_c3_mean"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c3_mean)))
    data_out["bb_counts_c4_mean"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c4_mean)))
    data_out["bb_counts_c5_mean"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c5_mean)))
    data_out["bb_counts_c3_std"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c3_std)))
    data_out["bb_counts_c4_std"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c4_std)))
    data_out["bb_counts_c5_std"] = (("time",), np.atleast_1d(np.squeeze(bb_counts_c5_std)))
    data_out["coef_calib_c3"] = (("time","coefs"), np.atleast_2d(coef_calib_c3))
    data_out["coef_calib_c4"] = (("time","coefs"), np.atleast_2d(coef_calib_c4))
    data_out["coef_calib_c5"] = (("time","coefs"), np.atleast_2d(coef_calib_c5))
    data_out["prt_counts"] = (("time","prts"), np.atleast_2d(prt_counts))
    data_out["prt_temp"] = (("time","prts"), np.atleast_2d(prt_temp))
    data_out["prt_temp_mean"] = (("time",), np.atleast_1d(np.squeeze(prt_temp_mean)))
    data_out["radiance_c3_radiance_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c3_radiance_bb)))
    data_out["radiance_c4_radiance_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c4_radiance_bb)))
    data_out["radiance_c5_radiance_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c5_radiance_bb)))
    data_out["radiance_c3_gain"] = (("time",), np.atleast_1d(np.squeeze(radiance_c3_gain)))
    data_out["radiance_c4_gain"] = (("time",), np.atleast_1d(np.squeeze(radiance_c4_gain)))
    data_out["radiance_c5_gain"] = (("time",), np.atleast_1d(np.squeeze(radiance_c5_gain)))
    data_out["radiance_c3_radiance_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c3_radiance_space)))
    data_out["radiance_c4_radiance_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c4_radiance_space)))
    data_out["radiance_c5_radiance_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c5_radiance_space)))
    data_out["radiance_c3_counts_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c3_counts_space)))
    data_out["radiance_c4_counts_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c4_counts_space)))
    data_out["radiance_c5_counts_space"] = (("time",), np.atleast_1d(np.squeeze(radiance_c5_counts_space)))
    data_out["radiance_c3_counts_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c3_counts_bb)))
    data_out["radiance_c4_counts_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c4_counts_bb)))
    data_out["radiance_c5_counts_bb"] = (("time",), np.atleast_1d(np.squeeze(radiance_c5_counts_bb)))
    data_out["ramp_c3"] = (("time",), np.atleast_1d(np.squeeze(ramp_c3)))
    data_out["ramp_c4"] = (("time",), np.atleast_1d(np.squeeze(ramp_c4)))
    data_out["ramp_c5"] = (("time",), np.atleast_1d(np.squeeze(ramp_c5)))
    data_out["space_counts_c3"] = (("time","positions"), np.atleast_2d(space_counts_c3))
    data_out["space_counts_c4"] = (("time","positions"), np.atleast_2d(space_counts_c4))
    data_out["space_counts_c5"] = (("time","positions"), np.atleast_2d(space_counts_c5))
    data_out["space_counts_c3_mean"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c3_mean)))
    data_out["space_counts_c4_mean"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c4_mean)))
    data_out["space_counts_c5_mean"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c5_mean)))
    data_out["space_counts_c3_std"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c3_std)))
    data_out["space_counts_c4_std"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c4_std)))
    data_out["space_counts_c5_std"] = (("time",), np.atleast_1d(np.squeeze(space_counts_c5_std)))
    data_out["temp_detector_radiator"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_radiator)))
    data_out["temp_detector_electronics"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_electronics)))
    data_out["temp_detector_cooler"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_cooler)))
    data_out["temp_detector_baseplate"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_baseplate)))
    data_out["temp_detector_motor"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_motor)))
    data_out["temp_detector_adconv"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_adconv)))
    data_out["temp_detector_patch"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_patch)))
    data_out["temp_detector_patch_extended"] = (("time",), np.atleast_1d(np.squeeze(temp_detector_patch_extended)))
    return data_out
    
if __name__ == "__main__":

    parser = OptionParser("usage: %prog launchcode year")
    (options, args) = parser.parse_args()
    if (len(args) < 1):
        launchcode = "NM"
        year = "2010"
    else:
        launchcode = args[0]
        year = int(args[1])

    path_in = set_path_in(launchcode,year)
    path_out = set_path_out(launchcode,year)
    orbit_list = generate_orbit_list(launchcode,year,path_in,path_out)
    file_vec = parse_orbit_list(orbit_list)

    df = []
#    for i in range(0,10):
    for i in range(len(file_vec)):

        file_in = file_vec[i]
        (timestamp, gd) = fix_datetime(path_in,file_in)    
        variables = mask_variables_time(timestamp,gd,path_in,file_in)
        ds = mask_variables_nan(timestamp,variables)
        df.append(ds)
        
    dataframe = xarray.concat(df, dim='time')        
    file_out = launchcode + '_' + year + '.nc'
    dataframe.to_netcdf(file_out)
    dataframe.close()



