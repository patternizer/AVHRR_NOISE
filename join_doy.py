#!/usr/bin/env python

# PROGRAM: join_doy.py

# call as: python join_doy.py instrument year
# degug: python -mipdb join_doy.py instrument year
# ----------------------------------------------------------------------------------
# Version 0.1
# 25 February, 2019
# michael.taylor AT reading DOT ac DOT uk

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
                   
def run(instrument,year):

    path_in = "/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper/" + instrument + "/" + str(year) + "/"
    file_out = path_in + instrument + "_" + str(year) + ".nc"

    if os.path.isdir(path_in):
        nclist = os.path.join(path_in,'*.nc')
        filelist = glob.glob(nclist)
        df = []
        for i in range(len(filelist)):

            file_in = str(filelist[i])
#            ds = xarray.open_dataset(file_in, decode_cf=True)
            ds = xarray.open_dataset(file_in)
            df.append(ds)
            
        data_out = xarray.concat(df, dim='time')
        data_out.to_netcdf(file_out)
        data_out.close()
        ds.close()    

if __name__ == "__main__":

    parser = OptionParser("usage: %prog instrument year")
    (options, args) = parser.parse_args()    
    instrument = args[0]
    year = int(args[1])
    run(instrument,year)
    



