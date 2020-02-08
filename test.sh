#!/bin/bash
# for running with `time ./test.sh` for performance testing

for i in {1..100}
do
	python poly_bat.py > /dev/null
done
