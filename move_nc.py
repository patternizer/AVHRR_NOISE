#!/usr/bin/env python

# PROGRAM: move_nc.py

# call as: python move_nc.py instrument year
# degug: python -mipdb move_nc.py instrument year
# ----------------------------------------------------------------------------------
# Version 0.1
# 27 February, 2019
# michael.taylor AT reading DOT ac DOT uk

import os
import os.path
import glob
import optparse
from  optparse import OptionParser 
import sys
import shutil
                   
def run(instrument,year):

    path_in = "/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_filtre/" + instrument + "/" + str(year) + "/"

    if os.path.isdir(path_in):

        for m in range(1,13):

#            month = str('{0:02d}'.format(m.astype('int64')))
            month = str('{0:02d}'.format(m))
            monthdir = path_in + month + "/"
            if os.path.isdir(monthdir):

#                os.chdir(monthdir)            
#               filelist = glob.iglob(os.path.join(monthdir, "*.data"))         
                filelist = os.listdir(monthdir)         
                for file in filelist:

                    shutil.move(file, path_in)
                    
if __name__ == "__main__":

    parser = OptionParser("usage: %prog instrument year")
    (options, args) = parser.parse_args()    
    instr = args[0]
    instrument = "values_" + instr
    year = int(args[1])
    run(instrument,year)
    



