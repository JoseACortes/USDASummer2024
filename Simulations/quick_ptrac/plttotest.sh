
echo ########
echo 'Running' detector_dfs_20_dfg_15
echo ########
echo ''
input_file=detector_dfs_20_dfg_15.inp

rm plotm.ps
mcnp6 ip i=$input_file notek com=plotcom
echo ''
ps2pdf plotm.ps plott.pdf
date