#! /bin/bash
ROUND=4
NAMES=(Aotizhongxin Changping Haidian Dongsi)
NUM=4

echo "K=1..................."
for ((n=0; n<$NUM; ++n))
do
echo ${NAMES[$n]}
    for ((i=1; i<$ROUND+1; ++i))  
    do
        FILE1=${NAMES[$n]}"_key1/station_"${NAMES[$n]}"_train"$i".txt"
        FILE2=${NAMES[$n]}"_key1/station_"${NAMES[$n]}"_test"$i".txt"
        python Evaluation.py $FILE1 $FILE2 1 
    done
done
echo "Beijing"
for ((i=1; i<$ROUND+1; ++i))  
do
    FILE1="Beijing_key1/city_Beijing_train"$i".txt"
    FILE2="Beijing_key1/city_Beijing_test"$i".txt"
    python Evaluation.py $FILE1 $FILE2 1 
done

echo "K=2...................."
for ((n=0; n<$NUM; ++n))
do
    echo ${NAMES[$n]}
    FILE1=${NAMES[$n]}"_key1/station_"${NAMES[$n]}".txt"
    FILE2=${NAMES[$n]}"_key2/station_"${NAMES[$n]}".txt"
    python Evaluation.py $FILE1 $FILE2 2 
done
echo "Beijing"
FILE1="Beijing_key1/city_Beijing.txt"
FILE2="Beijing_key2/city_Beijing.txt"
python Evaluation.py $FILE1 $FILE2 2 
