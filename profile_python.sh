#!/usr/bin/env bash

# use it with 'profile_python.sh yourname manage.py test -v app.tests.TestClass' for example
PROFILE_NAME=$1

shift

if [ ! -x gprof2dot ]
then pip install gprof2dot
fi

python -m cProfile -o $PROFILE_NAME.stats $*
OPTS="-n 4 -e 1"
gprof2dot -f pstats --wrap $OPTS $PROFILE_NAME.stats | dot -T png -o $PROFILE_NAME.png
