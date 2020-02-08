#!/bin/bash
# for running with `time ./test.sh` for performance testing

for i in {1..1000}
do
	python poly_bat.py > /dev/null
done
