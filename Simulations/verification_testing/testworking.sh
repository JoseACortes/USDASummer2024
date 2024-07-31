#!/bin/bash

#SBATCH --job-name=working
#SBATCH --account=auburn-mins
##SBATCH -p medium
##SBATCH --account=scinet
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=jose.cortes2@mavs.uta.edu
#SBATCH --nodes=1
#SBATCH --exclusive

#SBATCH --cpus-per-task=48

##SBATH -p priority --qos=nsdl
#SBATCH --time=168:00:00

atlas=false
n_tasks=23

for line in $(cat to_test.txt); do
    # if the line is a comment, skip it
    if [[ $line == \#* ]]; then
        continue
    fi
    echo ########
    echo 'Running' $line
    echo ########
    echo ''
    date

    input_file=input/$line.inp

    outp=output/outp/$line.outp
    runtpe=output/runtpe/$line.runtpe
    mctal=output/mctal/$line.mctal
    ptrac=output/ptrac/$line.ptrac

    rm $outp $mctal $runtpe #$ptrac
    echo 'Starting' $line

    if [ $atlas = true ]; then
        apptainer exec --pem-path=/home/jose.cortes/.ssh/mkey-pub.pem /apps/licensed/mcnp/mcnp-encrypted.sif mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
    else
        mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
    fi

    echo ''
    date
    echo ''

    python3 gen_graph.py $line
    echo 'Finished' $line
    echo ''
done