#! /bin/sh
echo "##########using eman2 to generate thumbnails##########"
source /home/jhdavis/.start_cd_conda.sh
source /home/jhdavis/.start_eman.sh
mkdir ./thumbs
for i in ./*_frames.mrc
do
	echo $i
	e2proc2d.py $i ./thumbs/$i.eman.jpg --process=filter.lowpass.gauss:cutoff_freq=0.1 --meanshrink=8
done
