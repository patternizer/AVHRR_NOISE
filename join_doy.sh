#!/bin/sh

FIDHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper
INMYVENV=${FIDHOME}/inmyvenv.sh
GENERATE=${FIDHOME}/join_doy.py
MEM_REQ=60000 # in MB
MEM_MAX=60000 # in MB 

join(){
    SAT=$1     
    START=$2 
    END=$3     
    for year in $(seq $START $END)  
    do
        JOBNAME="${SAT}${year}"
	LOGDIR="$FIDHOME/${SAT}/${year}/"	       
	if [ -d "$LOGDIR" ]; then
	    echo ${JOBNAME}
            LOGFILE=${LOGDIR}/run.log		    		   
 	    bsub -q short-serial -W24:00 -R "rusage[mem=$MEM_REQ]" -M $MEM_MAX -oo ${LOGFILE} -J "$JOBNAME" $INMYVENV $GENERATE "${SAT}" "${year}"
	fi
    done    
}

join NM 2002 2010
#join NL 2000 2010
wait

