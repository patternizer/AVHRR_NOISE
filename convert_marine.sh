#!/bin/bash

# Use python code to generate daily files from Marines ASCII files
# Output NetCDF4 files with internal compression
#
# Writes to directory $instr/$year
#
# Written By J.Mittaz University of Reading 20 Feb 2019
 
if [ $# -ne 3 ]
then
    echo "USAGE: ./convert_marine.sh instr(two character) year flag(y/n)"
    exit
fi

instr=$1
year=$2
flag=$3

#
# Take leap years into account
#
leap=1
if [ `expr $year % 400` -eq 0 ]; then
    leap=1
elif [ `expr $year % 100` -eq 0 ]; then
    leap=0
elif [ `expr $year % 4 ` -eq 0 ]; then
    leap=1
else
    leap=0
fi

if [ $leap -eq 0 ]; then
    ndays=365
else
    ndays=366
fi

yr=$(echo $year | awk '{ printf "%4.4d", $1 }')
mkdir -p $instr/$yr
cd $instr/$yr
ln -s ../../convert_marine.py .

for day in `seq 1 $ndays`
do
    script=$(echo $instr $year $day | awk '{ printf "run_%s_%4.4d_%3.3d.sh", $1, $2, $3 }')
    scriptlog=$(echo $instr $year $day | awk '{ printf "run_%s_%4.4d_%3.3d.log", $1, $2, $3 }')
    # --------------------------------------------------------------------------------------------------
    # MT: add --filtered flag to convert filtered data from essai_ss_filtre (otherwise from essai_filtre) 
    # --------------------------------------------------------------------------------------------------
    if [ $flag -eq 'n' ]; then
	echo "python convert_marine.py --day "$day "--complevel 9 "$instr" "$year > $script
    else
	echo "python convert_marine.py --filtered --day "$day "--complevel 9 "$instr" "$year > $script
    fi
    # --------------------------------------------------------------------------------------------------
    bsub -q short-serial -W24:00 -oo $scriptlog < $script
done

cd ../../

