import numpy as np

#pathname = "/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_filtre/values_NM/2002/"
pathname = "/Users/michaeltaylor/Desktop/AVHRR_NOISE/GITHUB/data/essai_filtre/NM_D10001.S0002/"
varname = "prt_counts"
datafile = varname + "_NM_D10001.S0002.data"
filename = pathname + datafile

data = np.loadtxt(filename, skiprows=1)
print(data)





