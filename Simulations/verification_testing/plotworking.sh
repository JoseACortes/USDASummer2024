for line in $(cat to_test.txt); do
    # if the line is a comment, skip it
    if [[ $line == \#* ]]; then
        continue
    fi
    echo ########
    echo 'Running' $line
    echo ########
    echo ''
    input_file=input/$line.inp
    outp=output/outp/plot_$line.outp
    comout=output/comout/$line.comout
    plotm=output/plot/plotm_$line.ps
    pdf=output/plot/plotm_$line.pdf

    rm $outp $comout $plotm
    rm plotm.ps
    mcnp6 ip i=$input_file notek com=plotcom comout=$comout outp=$outp
    cp plotm.ps $plotm
    rm plotm.ps
    echo ''
    ps2pdf $plotm $pdf
    date
done