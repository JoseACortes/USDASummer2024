#!/bin/bash

#SBATCH --job-name=detector_x_52_z_3
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

module load apptainer/1.1.9

line=detector_x_52_z_3

force_restart=true
n_tasks=96

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

if [ $force_restart = true ]; then
    rm $runtpe
fi

if [ -f $runtpe ]; then
    rm $outp
    echo 'Continuing' $line
    # check if the second line of a file is empty, if not add an empty line 
    awk 'NR==2{if($0 !~ /^ *$/){print "\n"$0; next}}1' $input_file > temp && mv temp $input_file
    echo ''
    apptainer exec --pem-path=/home/jose.cortes/.ssh/mkey-pub.pem /apps/licensed/mcnp/mcnp-encrypted.sif mcnp6 r c i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
    echo ''
    date
    echo ''
    exit
else
    rm $outp $mctal #$ptrac
    echo 'Starting' $line
    # check if the second line is empty, if so add an empty line
    awk 'NR==2{if($0 ~ /^ *$/){next}}1' $input_file > temp && mv temp $input_file
    apptainer exec --pem-path=/home/jose.cortes/.ssh/mkey-pub.pem /apps/licensed/mcnp/mcnp-encrypted.sif mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks

    echo ''
    date
    echo ''

fi

echo ''
date
echo ''