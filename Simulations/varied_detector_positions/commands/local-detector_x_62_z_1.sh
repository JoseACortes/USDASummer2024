line=detector_x_62_z_1

force_restart=false
n_tasks=5

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
    mcnp6 r c i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks
    echo ''
    date
    echo ''
    exit
else
    rm $outp $mctal #$ptrac
    echo 'Starting' $line
    # check if the second line is empty, if so add an empty line
    awk 'NR==2{if($0 ~ /^ *$/){next}}1' $input_file > temp && mv temp $input_file
    mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks

    echo ''
    date
    echo ''

fi