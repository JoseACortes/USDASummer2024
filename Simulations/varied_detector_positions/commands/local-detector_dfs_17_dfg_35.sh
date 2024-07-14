line=detector_dfs_17_dfg_35
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


rm $outp $mctal $runtpe #$ptrac
echo 'Starting' $line
mcnp6 r i=$input_file o=$outp mctal=$mctal ru=$runtpe notek tasks $n_tasks

echo ''
date
echo ''