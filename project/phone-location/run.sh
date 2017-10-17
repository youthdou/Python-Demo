#!/bin/bash

echo "Start running"
source ~/demo3/bin/activate
#python --version
echo $(cd `dirname $0`; pwd)
for i in $(seq 1 5)
do
    #echo $i
    #python $(cd `dirname $0`; pwd)/bash-demo.sh
    #python bash-test.py
    python compare_phonelocation.py
done
echo "End"