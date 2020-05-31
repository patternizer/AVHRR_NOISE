#!/bin/sh

#FIDHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/group_workspaces/cems2/fiduceo/Users/mdesmons/avhrr_l1b/essai_filtre
FIDHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper
INMYVENV=${FIDHOME}/inmyvenv.sh
GENERATE=${FIDHOME}/move_nc.py
MEM_REQ=10000 # in MB
MEM_MAX=10000 # in MB 

move(){
    SAT=$1     
    START=$2 
    END=$3     
    for year in $(seq $START $END)  
    do
        JOBNAME="${SAT}${year}"
	LOGDIR="$FIDHOME"
	echo ${JOBNAME}
        LOGFILE=${LOGDIR}/run.log
 	bsub -q short-serial -W24:00 -R "rusage[mem=$MEM_REQ]" -M $MEM_MAX -oo ${LOGFILE} -J "$JOBNAME" $INMYVENV $GENERATE "${SAT}" "${year}"
    done    
}

move NM 2002 2010
wait

