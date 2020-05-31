from __future__ import print_function,division
import numpy as np
import netCDF4 as nc
import os
import calendar
import datetime
import xarray as xr
import argparse
import glob
import time


# Read in relevant files (ASCII data files)

def read_directory(top_level,instr,year):
    '''
    Read in date_* files in a directory
    
    top_level = top level directory
    instr     = two letter name based on original AVHRR pre-launch data
    year      = year to read in
    '''

    #
    # search string for files
    #
    search_dir = '{0}/values_{1}/{2:04d}'.\
        format(top_level,instr,year)
    search_string = '{0}/values_{1}/{2:04d}/date_{1}_*'.\
        format(top_level,instr,year)

    #
    # get filelist
    #
    filelist = glob.glob(search_string)
    if filelist is None:
        raise Exception('Cannot file files : searchstring : {0}'.\
                            format(search_string))
    elif len(filelist) == 0:
        raise Exception('Cannot file files : searchstring : {0}'.\
                            format(search_string))
    else:
        filelist.sort()

    return filelist,search_dir

#
# Convert date arrays to datetime
#
def get_datetime(data,orig_time):

    year = data[:,0].astype(np.int32)
    month = data[:,1].astype(np.int32)
    day = data[:,2].astype(np.int32)
    hours = data[:,4]
    hr = hours.astype(np.int32)
    temp = (hours - hr)*60.
    mn = temp.astype(np.int32)
    temp = (temp - mn)*60.
    sc = temp.astype(np.int32)
    msec = ((temp - sc)*1e6).astype(np.int32)
    
    #
    # Covert to datetime
    #
    date = []
    for i in range(len(year)):
        date.append(nc.date2num(datetime.datetime(year[i],month[i],day[i],hr[i],mn[i],sc[i],msec[i]),orig_time))       
    return np.array(date)

#
# Reset bad counts data to -1e30 or -32768
# counts to -32768, mean/std to -1e30
# 
def reset_counts_float(data):

    newdata1 = data[:,0:10]
    gd = (newdata1 < 0) | ~np.isfinite(newdata1)
    if np.sum(gd) > 0:
        newdata1[gd] = -32768
    newdata2 = data[:,10]
    gd = (newdata2 < 0) | ~np.isfinite(newdata2)
    if np.sum(gd) > 0:
        newdata2[gd] = -1e30
    newdata3 = data[:,11]
    gd = (newdata3 < 0) | ~np.isfinite(newdata3)
    if np.sum(gd) > 0:
        newdata3[gd] = -1e30
    
    data[:,0:10] = newdata1
    data[:,10] = newdata2
    data[:,11] = newdata3

    return data
#
# Reset bad data to -1e30 or -32768
# 
def reset_bad_data(data):

#
# MT: add additional filtered variables: 
#     bright_temp
#     earth_bt_fiduceo 
#     earth_counts
#     earth_radiance_fiduceo
#     latitudes
#     longitudes
 

    #
    # bright_temp
    #
    counts_name = ['bright_temp_c3','bright_temp_c4','bright_temp_c5']
    for name in counts_name:
        new_data = {name:reset_counts_float(data[name])}
        data.update(new_data)

    #
    # earth_bt_fiduceo
    #
    counts_name = ['earth_bt_fiduceo_c3','earth_bt_fiduceo_c4','earth_bt_fiduceo_c5']
    for name in counts_name:
        new_data = {name:reset_counts_float(data[name])}
        data.update(new_data)

    #
    # earth_counts
    #
    counts_name = ['earth_counts_c3','earth_counts_c4','earth_counts_c5']
    for name in counts_name:
        new_data = {name:reset_counts_float(data[name])}
        data.update(new_data)

    #
    # earth_radiance_fiduceo
    #
    counts_name = ['earth_radiance_fiduceo_c3','earth_radiance_fiduceo_c4','earth_radiance_fiduceo_c5']
    for name in counts_name:
        new_data = {name:reset_counts_float(data[name])}
        data.update(new_data)

    #
    # Latitudes
    #
    newdata = data['latitudes'][:,:]
    gd = (newdata < 0) | ~np.isfinite(newdata)
    if np.sum(gd) > 0:
        newdata[gd] = -1e30
    new_data = {'temp_prt':newdata}
    data.update(new_data)

    #
    # Longitudes
    #
    newdata = data['longitudes'][:,:]
    gd = (newdata < 0) | ~np.isfinite(newdata)
    if np.sum(gd) > 0:
        newdata[gd] = -1e30
    new_data = {'temp_prt':newdata}
    data.update(new_data)



    #
    # BB/Sp counts
    #
    counts_name = ['bb_counts_c3','bb_counts_c4','bb_counts_c5','space_counts_c3','space_counts_c4','space_counts_c5']
    for name in counts_name:
        new_data = {name:reset_counts_float(data[name])}
        data.update(new_data)

    #
    # Coef calibration values
    #
    rad_name = ['coef_calib_c3','coef_calib_c4','coef_calib_c5']
    for name in rad_name:
        newdata = data[name][:,:]
        gd = (newdata < -1e20) | ~np.isfinite(newdata)
        if np.sum(gd) > 0:
            newdata[gd] = -1e30
        new_data = {name:newdata}
        data.update(new_data)

    #
    # PRT counts
    #
    newdata = data['prt_counts'][:,:]
    gd = (newdata < 0) | ~np.isfinite(newdata)
    if np.sum(gd) > 0:
        newdata[gd] = -32768
    new_data = {'prt_counts': newdata}
    data.update(new_data)
    
    #
    # Radiance
    #
    rad_name = ['radiance_c3','radiance_c4','radiance_c5']
    for name in rad_name:
        newdata = data[name][:,:]
        gd = (newdata < 0) | ~np.isfinite(newdata)
        if np.sum(gd) > 0:
            newdata[gd] = -1e30
        new_data = {name:newdata}
        data.update(new_data)
        
    #
    # Ramp
    #
    rad_name = ['ramp_c3','ramp_c4','ramp_c5']
    for name in rad_name:
        newdata = data[name][:]
        gd = (newdata < 0) | ~np.isfinite(newdata)
        if np.sum(gd) > 0:
            newdata[gd] = -1e30
        new_data = {name:newdata}
        data.update(new_data)

    #
    # Temperatures
    #
    newdata = data['temp_detector'][:,:]
    gd = (newdata < 0) | ~np.isfinite(newdata)
    if np.sum(gd) > 0:
        newdata[gd] = -1e30
    new_data = {'temp_detector':newdata}
    data.update(new_data)

    #
    # Temperatures PRT
    #
    newdata = data['temp_prt'][:,:]
    gd = (newdata < 0) | ~np.isfinite(newdata)
    if np.sum(gd) > 0:
        newdata[gd] = -1e30
    new_data = {'temp_prt':newdata}
    data.update(new_data)

    return data
#
# Reformat data to ensure sensible data types and fill values
#
def reformat_data(indata_all,filename,complevel=-1):

    #
    # Reset bad data to -1e30 for FillValues
    #
    indata = reset_bad_data(indata_all)

    #
    # Date in datetime format
    #    
    timesecs = get_datetime(indata['date'],'seconds since 1970-01-01:00:00:00')

    #
    # Start dataset
    #
    data = xr.Dataset({"time":(("time",), timesecs)})
    data["time"].attrs["units"] ='seconds since 1970-01-01:00:00:00'
    data["positions"] = (("positions"),np.arange(0,10))
    data["coefs"] = (("coefs"),np.arange(0,3))
    data["prts"] = (("prts"),np.arange(0,4))

    #
    # BB counts
    #
    data["bb_counts_c3"] = (("time","positions"),indata['bb_counts_c3'][:,0:10].astype(np.int16))
    data["bb_counts_c3"].attrs["_FillValue"] = -32768
    data["bb_counts_c3_mean"] = (("time",),indata['bb_counts_c3'][:,10].astype(np.float32))
    data["bb_counts_c3_mean"].attrs["_FillValue"] = -1e30
    data["bb_counts_c3_std"] = (("time",),indata['bb_counts_c3'][:,11].astype(np.float32))
    data["bb_counts_c3_std"].attrs["_FillValue"] = -1e-30
    data["bb_counts_c4"] = (("time","positions"),indata['bb_counts_c4'][:,0:10].astype(np.int16))
    data["bb_counts_c4"].attrs["_FillValue"] = -32768
    data["bb_counts_c4_mean"] = (("time",),indata['bb_counts_c4'][:,10].astype(np.float32))
    data["bb_counts_c4_mean"].attrs["_FillValue"] = -1e30
    data["bb_counts_c4_std"] = (("time",),indata['bb_counts_c4'][:,11].astype(np.float32))
    data["bb_counts_c4_std"].attrs["_FillValue"] = -1e30
    data["bb_counts_c5"] = (("time","positions"),indata['bb_counts_c5'][:,0:10].astype(np.int16))
    data["bb_counts_c5"].attrs["_FillValue"] = -32768
    data["bb_counts_c5_mean"] = (("time",),indata['bb_counts_c5'][:,10].astype(np.float32))
    data["bb_counts_c5_mean"].attrs["_FillValue"] = -1e30
    data["bb_counts_c5_std"] = (("time",),indata['bb_counts_c5'][:,11].astype(np.float32))
    data["bb_counts_c5_std"].attrs["_FillValue"] = -1e30

    #
    # space counts
    #
    data["space_counts_c3"] = (("time","positions"),\
                                   indata['space_counts_c3'][:,0:10].\
                                   astype(np.int16))
    data["space_counts_c3"].attrs["_FillValue"] = -32768
    data["space_counts_c3_mean"] = (("time",),\
                                        indata['space_counts_c3'][:,10].\
                                        astype(np.float32))
    data["space_counts_c3_mean"].attrs["_FillValue"] = -1e30
    data["space_counts_c3_std"] = (("time",),\
                                       indata['space_counts_c3'][:,11].\
                                       astype(np.float32))
    data["space_counts_c3_std"].attrs["_FillValue"] = -1e30

    data["space_counts_c4"] = (("time","positions"),\
                                   indata['space_counts_c4'][:,0:10].\
                                   astype(np.int16))
    data["space_counts_c4"].attrs["_FillValue"] = -32768
    data["space_counts_c4_mean"] = (("time",),\
                                        indata['space_counts_c4'][:,10].\
                                        astype(np.float32))
    data["space_counts_c4_mean"].attrs["_FillValue"] = -1e30
    data["space_counts_c4_std"] = (("time",),\
                                       indata['space_counts_c4'][:,11].\
                                       astype(np.float32))
    data["space_counts_c4_std"].attrs["_FillValue"] = -1e30

    data["space_counts_c5"] = (("time","positions"),\
                                   indata['space_counts_c5'][:,0:10].\
                                   astype(np.int16))
    data["space_counts_c5"].attrs["_FillValue"] = -32768
    data["space_counts_c5_mean"] = (("time",),\
                                        indata['space_counts_c5'][:,10].\
                                        astype(np.float32))
    data["space_counts_c5_mean"].attrs["_FillValue"] = -1e30
    data["space_counts_c5_std"] = (("time",),\
                                       indata['space_counts_c5'][:,11].\
                                       astype(np.float32))
    data["space_counts_c5_std"].attrs["_FillValue"] = -1e30


    #
    # Calibration coefficients
    #
    data["coef_calib_c3"] = (("time","coefs"),\
                                   indata['coef_calib_c3'][:,:].\
                                   astype(np.float32))
    data["coef_calib_c3"].attrs["_FillValue"] = -1e30
    data["coef_calib_c4"] = (("time","coefs"),\
                                   indata['coef_calib_c4'][:,:].\
                                   astype(np.float32))
    data["coef_calib_c4"].attrs["_FillValue"] = -1e30
    data["coef_calib_c5"] = (("time","coefs"),\
                                   indata['coef_calib_c5'][:,:].\
                                   astype(np.float32))
    data["coef_calib_c5"].attrs["_FillValue"] = -1e30


    #
    # PRT counts
    # Have to force -1e30 to something sensible for fill value
    # Split into the three PRT measurements and indexing
    #
    prt_counts = indata['prt_counts'][:,:]
    gd = (prt_counts < -1)
    prt_counts[gd] = -32768.
    data["prt_counts"] = (("time","prts"),\
                              indata['prt_counts'][:,0:4].\
                              astype(np.int16))
    data["prt_counts"].attrs["_FillValue"] = -32768

    #
    # Radiance arrays
    #
    # BB
    #
    data["radiance_c3_radiance_bb"] = (("time",),\
                                           indata['radiance_c3'][:,0].\
                                           astype(np.float32))
    data["radiance_c3_radiance_bb"].attrs["_FillValue"] = -1e30
    data["radiance_c4_radiance_bb"] = (("time",),\
                                           indata['radiance_c4'][:,0].\
                                           astype(np.float32))
    data["radiance_c4_radiance_bb"].attrs["_FillValue"] = -1e30
    data["radiance_c5_radiance_bb"] = (("time",),\
                                           indata['radiance_c5'][:,0].\
                                           astype(np.float32))
    data["radiance_c5_radiance_bb"].attrs["_FillValue"] = -1e30
    #
    # Gain 
    #
    data["radiance_c3_gain"] = (("time",),\
                                           indata['radiance_c3'][:,1].\
                                           astype(np.float32))
    data["radiance_c3_gain"].attrs["_FillValue"] = -1e30
    data["radiance_c4_gain"] = (("time",),\
                                           indata['radiance_c4'][:,1].\
                                           astype(np.float32))
    data["radiance_c4_gain"].attrs["_FillValue"] = -1e30
    data["radiance_c5_gain"] = (("time",),\
                                           indata['radiance_c5'][:,1].\
                                           astype(np.float32))
    data["radiance_c5_gain"].attrs["_FillValue"] = -1e30  

    #
    # Radiance of space
    #
    data["radiance_c3_space"] = (("time",),\
                                           indata['radiance_c3'][:,2].\
                                           astype(np.float32))
    data["radiance_c3_space"].attrs["_FillValue"] = -1e30
    data["radiance_c4_space"] = (("time",),\
                                           indata['radiance_c4'][:,2].\
                                           astype(np.float32))
    data["radiance_c4_space"].attrs["_FillValue"] = -1e30
    data["radiance_c5_space"] = (("time",),\
                                           indata['radiance_c5'][:,2].\
                                           astype(np.float32))
    data["radiance_c5_space"].attrs["_FillValue"] = -1e30
    #
    # BB view mean 
    #
    data["radiance_c3_counts_bb"] = (("time",),\
                                           indata['radiance_c3'][:,3].\
                                           astype(np.float32))
    data["radiance_c3_counts_bb"].attrs["_FillValue"] = -1e30
    data["radiance_c4_counts_bb"] = (("time",),\
                                           indata['radiance_c4'][:,3].\
                                           astype(np.float32))
    data["radiance_c4_counts_bb"].attrs["_FillValue"] = -1e30
    data["radiance_c5_counts_bb"] = (("time",),\
                                           indata['radiance_c5'][:,3].\
                                           astype(np.float32))
    data["radiance_c5_counts_bb"].attrs["_FillValue"] = -1e30

    #
    # Sp view mean 
    #
    data["radiance_c3_counts_sp"] = (("time",),\
                                           indata['radiance_c3'][:,4].\
                                           astype(np.float32))
    data["radiance_c3_counts_sp"].attrs["_FillValue"] = -1e30
    data["radiance_c4_counts_sp"] = (("time",),\
                                           indata['radiance_c4'][:,4].\
                                           astype(np.float32))
    data["radiance_c4_counts_sp"].attrs["_FillValue"] = -1e30
    data["radiance_c5_counts_sp"] = (("time",),\
                                           indata['radiance_c5'][:,4].\
                                           astype(np.float32))
    data["radiance_c5_counts_sp"].attrs["_FillValue"] = -1e30

    #
    # Ramp
    #
    data["ramp_c3"] = (("time",),\
                           indata['ramp_c3'][:].\
                           astype(np.float32))
    data["ramp_c3"].attrs["_FillValue"] = -1e30
    data["ramp_c4"] = (("time",),\
                           indata['ramp_c4'][:].\
                           astype(np.float32))
    data["ramp_c4"].attrs["_FillValue"] = -1e30
    data["ramp_c5"] = (("time",),\
                           indata['ramp_c5'][:].\
                           astype(np.float32))
    data["ramp_c5"].attrs["_FillValue"] = -1e30
    

    #
    # Temperatures
    #
    data["temp_detector_radiator"] = (("time",),\
                                          indata['temp_detector'][:,0].\
                                          astype(np.float32))
    data["temp_detector_radiator"].attrs["_FillValue"] = -1e30
    data["temp_detector_electronics"] = (("time",),\
                                             indata['temp_detector'][:,1].\
                                             astype(np.float32))
    data["temp_detector_radiator"].attrs["_FillValue"] = -1e30
    data["temp_detector_cooler"] = (("time",),\
                                        indata['temp_detector'][:,2].\
                                        astype(np.float32))
    data["temp_detector_cooler"].attrs["_FillValue"] = -1e30
    data["temp_detector_baseplate"] = (("time",),\
                                           indata['temp_detector'][:,3].\
                                           astype(np.float32))
    data["temp_detector_baseplate"].attrs["_FillValue"] = -1e30
    data["temp_detector_motor"] = (("time",),\
                                       indata['temp_detector'][:,4].\
                                       astype(np.float32))
    data["temp_detector_motor"].attrs["_FillValue"] = -1e30
    data["temp_detector_adconv"] = (("time",),\
                                        indata['temp_detector'][:,5].\
                                        astype(np.float32))
    data["temp_detector_adconv"].attrs["_FillValue"] = -1e30
    data["temp_detector_patch"] = (("time",),\
                                        indata['temp_detector'][:,6].\
                                       astype(np.float32))
    data["temp_detector_patch"].attrs["_FillValue"] = -1e30
    data["temp_detector_patch_extended"] = (("time",),\
                                                indata['temp_detector'][:,7].\
                                                astype(np.float32))
    data["temp_detector_patch_extended"].attrs["_FillValue"] = -1e30

    #
    # PRT temperatures
    #
    data["temp_prt"] = (("time","prts"),indata['temp_prt'][:,0:4].astype(np.float32))
    data["temp_prt"].attrs["_FillValue"] = -1e30
    
    #
    # Add compression if requested
    #
    if complevel > 0:
        comp = dict(zlib=True, complevel=complevel, shuffle=True)
        encoding = {var: comp for var in data.data_vars}
        data.to_netcdf(filename, encoding=encoding)
    else:
        data.to_netcdf(filename)

#
# Check to see if all files are available
# Also check file size
#
def all_files_there(directory,file_stem,type_name):

    ok = True
    for typename in type_name:
        filename = directory+'/'+typename+file_stem
        #
        # If not found check not a system access issue but waiting
        #
        if not os.path.exists(filename):
            time.sleep(1)
            if not os.path.exists(filename):
                ok = False
        if ok:
            statinfo = os.stat(filename)
            if statinfo.st_size < 1000:
                ok = False
    return ok
#
# Convert to NetCDF files
#
# Makes a dictionary with 1 days worth of data from the different files
#
# Outputs a single netCDF file
#

# -----------------------------------------
# MT: add input flag for changing top_level
# -----------------------------------------
# def convert_files(instr,year,alldays=True,complevel=6,day=-1,monthly=False):
def convert_files(instr,year,alldays=True,complevel=6,day=-1,monthly=False,filtered=False):
# -----------------------------------------
    '''
    Top level routine to run though a given instrument and year
    alldays = True means do a complete year
    alldays - False means individual days are output
    filtered - True means process data from essai_ss_filtre/
    filtered = False means process data from essai_filtre/
    '''

    # -----------------------------------------------------------------------------------
    # MT: add logic to direct top_level to either filtered or unfiltered data directories
    # -----------------------------------------------------------------------------------
    # top_level='/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_ss_filtre'
    if filtered:
        top_level='/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_ss_filtre'
    else: 
        top_level='/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_filtre'
    # -----------------------------------------------------------------------------------

    #
    # List of variables to get and their file end
    #
    type_name = ['bb_counts_c3',\
                 'bb_counts_c4',\
                 'bb_counts_c5',\
                 'coef_calib_c3',\
                 'coef_calib_c4',\
                 'coef_calib_c5',\
                 'prt_counts',\
                 'radiance_c3',\
                 'radiance_c4',\
                 'radiance_c5',\
                 'ramp_c3',\
                 'ramp_c4',\
                 'ramp_c5',\
                 'space_counts_c3',\
                 'space_counts_c4',\
                 'space_counts_c5',\
                 'temp_detector',\
                 'temp_prt']
    #
    # Different files have different numbers of headers
    # This gives how many lines to skip
    #
    file_nhead = [1,1,1,\
                  1,0,0,\
                  1,\
                  1,1,1,\
                  0,0,0,\
                  1,1,1,\
                  1,\
                  1]
                      
    #
    # Get date_* files
    #
    filelist_total,search_dir = read_directory(top_level,instr,year)    
    if len(filelist_total) == 0:
        raise Excetion('No filed found')

    #
    # Loop round dats in year and select those in list that match
    #
    if calendar.isleap(year):
        tot_days = 366
    else:
        tot_days = 365
    #
    # Make sure year is 2 digit only
    #
    if year > 100:
        if year < 2000:
            yr = year - 1900
        else:
            yr = year - 2000
    else:
        yr = year
    start = False
    data_accrued = False
    month_stored = -1
    if day > 0:
        start_days = day-1
        tot_days = start_days+1
    else:
        start_days = 0        
    for dayno in range(start_days,tot_days):
        #
        # Get date filter string and datetime variable
        #
        test_date = 'D{0:02d}{1:03d}'.format(yr,dayno+1)
        current_date = datetime.datetime.strptime('{0:04d}-{1:03d}'.format(year,dayno+1),'%Y-%j')
        #
        # Get elements to total filelist which satisfy this string
        #
        filelist = [s for s in filelist_total if test_date in s]
        if len(filelist) == 0:
            print('Cannot file files for search string : {0}'.format(test_date))
            print('In directory : {0}'.format(search_dir))
        if len(filelist) > 0:
            
            #
            # If write out monthly data then do so if month has mooved on
            #
            if monthly and alldays:
                if data_accrued and month_store > 0 and current_time.month != month_store:
                    #
                    # Output specific month
                    #
                    ofile = '{0}_{1:04d}_M{2:02d}.nc'.format(instr,year,month)
                    reformat_data(data,ofile,complevel=complevel)
            #
            # Loop round files and read different variables
            #
            if alldays and monthly and month != month_store:
                start = False
            elif not alldays:
                start = False
            for filename in filelist:
                #
                # Get directory and file_step to use with other variables 
                # than date
                #
                directory,file_name = os.path.split(filename) 
                file_stem = file_name[4:25]
                #
                # Check to see if for this file we have all files needed
                #
                if not all_files_there(directory,file_stem,type_name):
                    continue
                #
                # If all there, then get
                #
                if not start:
                    #
                    # Read in date arrays
                    #
                    print('filename:',filename)
                    #
                    # Some problem with file access
                    # If file not there wait for 1 second and try again
                    #
                    if os.path.exists(filename):
                        d = np.loadtxt(filename,skiprows=1)
                    else:
                        time.sleep(1)
                        d = np.loadtxt(filename,skiprows=1)
                    #
                    # Get list of good dates
                    #
                    gd = (d[:,0] > 0)
                    #
                    # Start dictionary
                    #
                    data = {'date':d[gd,:]}
                    #
                    # Loop over type_name and load dictionary
                    #
                    for i in range(len(type_name)):
                        newfile = directory+'/'+type_name[i]+file_stem
                        if os.path.exists(newfile):
                            d = np.loadtxt(newfile,skiprows=file_nhead[i])
                        else:
                            time.sleep(1)
                            d = np.loadtxt(newfile,skiprows=file_nhead[i])
                        if len(d.shape) == 1:
                            data[type_name[i]] = d[gd]
                        else:
                            data[type_name[i]] = d[gd,:]
                    start=True
                    data_accrued=True
                else:
                    #
                    # Read in date arrays
                    #
                    print('filename:',filename)
                    d = np.loadtxt(filename,skiprows=1)
                    #
                    # Get list of good dates
                    #
                    gd = (d[:,0] > 0)
                    #
                    # Add to dictionary element
                    #
                    newdata = {'date':np.append(data['date'],d[gd,:],axis=0)}
                    data.update(newdata)
                    #
                    # Loop round type_name and append to dictionary
                    #
                    for i in range(len(type_name)):
                        newfile = directory+'/'+type_name[i]+file_stem
                        if os.path.exists(newfile):
                            d = np.loadtxt(newfile,skiprows=file_nhead[i])
                        else:
                            time.sleep(1)
                            d = np.loadtxt(newfile,skiprows=file_nhead[i])
                        if len(d.shape) == 1:
                            newdata = {type_name[i]:np.append(data[type_name[i]],d[gd],axis=0)}
                        else:
                            newdata = {type_name[i]:np.append(data[type_name[i]],d[gd,:],axis=0)}
                        data.update(newdata)
                    data_accrued = True
            month_stored = current_date.month
            if not alldays and data_accrued:
                #
                # Split out cases with integer only values and means
                # and set fill values for netCDF generation
                #
                # Output data
                #
                #
                ofile = '{0}_D{1:02d}{2:03d}.nc'.format(instr,yr,dayno+1)
                reformat_data(data,ofile,complevel=complevel)

    if alldays and data_accrued:
        if day == -1 and month == -1:
            #
            # Output individual days
            #
            ofile = '{0}_{1:04d}_D{2:03d}.nc'.format(instr,year,dayno+1)
            reformat_data(data,ofile,complevel=complevel)
        elif day > 0:
            #
            # Output specific day
            #
            ofile = '{0}_{1:04d}_D{2:03d}.nc'.format(instr,year,dayno+1)
            reformat_data(data,ofile,complevel=complevel)
            return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert Marines ASCII to netcdf')
    parser.add_argument('instr', nargs=1,
                        help='Two letter AVHRR code (pre-launch) e.g. NM (NOAA-17)')
    parser.add_argument('year', type=int, nargs=1,
                        help='year of data to get')
    parser.add_argument('--daily', action='store_true',
                        help='get individual days')
    parser.add_argument('--day', type=int, nargs=1, default=-1,
                        help='get files for individual day')
    parser.add_argument('--monthly', action='store_true',
                        help='get files for separate months')
    parser.add_argument('--complevel', type=int, nargs=1, default=-1,
                        help='compression level (defaults to none)')
    # -----------------------------------------------------------------------------------
    # MT: add option to direct to_level to either filtered or unfiltered data directories
    # -----------------------------------------------------------------------------------
    parser.add_argument('--filtered', action='store_true',
                        help='get filtered data')
    # -----------------------------------------------------------------------------------

    args = parser.parse_args()
    instr = args.instr[0]
    year = args.year[0]
    try:
        complevel = args.complevel[0]
    except:
        complevel = -1
    try:
        day = args.day[0]
    except:
        day = -1

    # -----------------------------------------------------------------------------------
    # MT: add option to direct to_level to either filtered or unfiltered data directories
    # -----------------------------------------------------------------------------------

    # if args.daily:
    #     convert_files(instr,year,alldays=False,complevel=complevel)
    # elif args.monthly:
    #     convert_files(instr,year,alldays=True,monthly=True,complevel=complevel)
    # elif day >= 1:
    #     convert_files(instr,year,alldays=True,monthly=False,day=day,complevel=complevel)
    # else:
    #     convert_files(instr,year,complevel=complevel)

    if args.filtered:
        if args.daily:
            convert_files(instr,year,alldays=False,filtered=True,complevel=complevel)
        elif args.monthly:
            convert_files(instr,year,alldays=True,monthly=True,filtered=True,complevel=complevel)
        elif day >= 1:
            convert_files(instr,year,alldays=True,monthly=False,day=day,filtered=True,complevel=complevel)
        else:
            convert_files(instr,year,filtered=True,complevel=complevel)
    else:
        if args.daily:
            convert_files(instr,year,alldays=False,complevel=complevel)
        elif args.monthly:
            convert_files(instr,year,alldays=True,monthly=True,complevel=complevel)
        elif day >= 1:
            convert_files(instr,year,alldays=True,monthly=False,day=day,complevel=complevel)
        else:
            convert_files(instr,year,complevel=complevel)

    # -----------------------------------------------------------------------------------
