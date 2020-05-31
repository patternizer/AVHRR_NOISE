#!/bin/sh

FIDHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper
INMYVENV=${FIDHOME}/inmyvenv.sh
GENERATE=${FIDHOME}/convert_marine.sh
MEM_REQ=60000 # in MB
MEM_MAX=60000 # in MB 

convert(){
    SAT=$1     
    START=$2 
    END=$3     
    FLAG=$4
    for year in $(seq $START $END)  
    do
        JOBNAME="${SAT}${year}${FLAG}"
	LOGFILE=$(echo $SAT $year $FLAG | awk '{ printf "run.%s_%4.4d_%s.log", $1, $2, $3}')
	LOGDIR="$FIDHOME"	       
	if [ -d "$LOGDIR" ]; then
#	    echo ${JOBNAME}
            LOGFILE=${LOGDIR}/${LOGFILE}		    		   
 	    bsub -q short-serial -W24:00 -R "rusage[mem=$MEM_REQ]" -M $MEM_MAX -oo ${LOGFILE} -J "$JOBNAME" $INMYVENV $GENERATE "${SAT}" "${year}" "${FLAG}"
	fi
    done    
}

convert NL 2000 2010 n
convert NM 2002 2010 y
wait


