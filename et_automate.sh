#!/bin/sh

ETHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/essai_ss_filtre
#ETHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/GWS_ADMIN/ET/essai_filtre
FIDHOME=/gws/nopw/j04/fiduceo/Users/mtaylor/noise_paper
INMYVENV=${FIDHOME}/inmyvenv.sh
GENERATE=${FIDHOME}/convert_marine.sh
MEM_REQ=60000 # in MB
MEM_MAX=60000 # in MB 

#
# Form bsub to submit convert_marine.sh at sensor/year-level for retrieved batch
#
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


# --------------------------------------------
# ELASTIC TAPE MANAGEMENT ROUTINE
# --------------------------------------------

#
# Get list of batches on ET-WORKSPACE=fiduceo:
#
et_ls.py -w fiduceo -H -L batch > et_batchlist.txt

#
# Get sub-list of Marine's directories on ET containing filtered data:
#
grep "MD_essai_ss_filtre" et_batchlist.txt > batchlist_ss_filtre.txt
rm et_batchlist.txt

#
# Get number of batches to retrieve:
#
N="$(wc -l "batchlist_ss_filtre.txt" | awk '{print $1}')"

#
# Form BATCH_ID array
#
#BATCH_IDS="$(cat "batchlist_ss_filtre.txt" | awk '{print $2}')"
BATCH_IDS=( )
while IFS= read -r -d '' "$(awk '{print $2}')"
do
  BATCH_IDS+=( "$(awk '{print $2}')" )
done < batchlist_ss_filtre.txt
#echo "${BATCH_IDS}"

#
# Form BATCH_DIR array
#
#BATCH_DIRS="$(cat "batchlist_ss_filtre.txt" | awk '{print $8}')"
BATCH_DIRS=( )
while IFS= read -r -d '' "$(awk '{print $8}')"
do
  BATCH_DIRS+=( "$(awk '{print $8}')" )
done < batchlist_ss_filtre.txt
#echo "${BATCH_DIRS}"

# -----------------------
# MAIN LOOP
# -----------------------

#
# Loop over batches and poll RSS feed until each retrieval is complete
#
for (( i=1; i<=$N; i++ ))
do
    BATCH_ID=$BATCH_IDS[$i]
    BATCH_DIR=$ETDIR/$BATCH_DIRS[$i]/
    mkdir $BATCH_DIR
    BATCH_LOG=$BATCH_ID.log
    #
    # Retrieve batch from ET:
    #
    # nohup et_get.py -v -w fiduceo -b ${BATCH_ID} -r ${BATCH_DIR} > ${BATCH_LOG} &   
    #
    # Ping ET-RSS feed to test for completion of retrieval:
    #
    completed=0
    RSS="http://et-monitor.fds.rl.ac.uk/et_rss/ET_RSS_AlertWatch_atom.php?workspace=fiduceo"
    until [ $completed -gt 0 ]
    do
	curl $RSS | sed -e 's$<$\n<$g' | grep description | grep "mtaylor" | grep -e completed -e batch | while read line
	do
	    echo $line
	    # 
	    # NEED TO CODE:
	    # ------------
	    # grep on batch number --> process ID
	    # grep on process ID --> completed $BATCH
	    # 
	    if [ $BATCH -eq $BATCH_ID ]; then
		completed=`expr $completed + 1`
	    else
		completed=0
	    fi 
	done
	sleep 1
	echo "Waiting for the ET retrieval to complete ..."
	completed=1
    done
    echo "ET retrieval of batch $BATCH_ID is complete"
    # 
    # NEED TO CODE:
    # ------------
    # Get arguments for call to bsub:
    # 
    # YEAR1 = $(grep ls $BATCH_DIR | head -1)
    # YEAR2 = $(grep ls $BATCH_DIR | tail -1)
    # INSTR = $BATCH_DIR --> extract 2 letter launchcode 

    #
    # Convert batch from ASCII --> netCDF
    #
    convert ${INSTR} ${YEAR1} ${YEAR2} y

    #
    # Concatenate converted netCDFs --> yearly summaries
    #
    ./join_doy.sh ${INSTR}

    #
    # Concatenate yearly summaries --> sensor timeseries
    #
    ./join_year.sh ${INSTR}


done
wait



