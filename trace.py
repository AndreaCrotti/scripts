#!/usr/bin/env python
import trace
import sys

# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix,], trace=0,
                  count=1)
# run the new command using the given tracer
tracer.run('main()')
# make a report, placing output in /tmp
r = tracer.results()
r.write_results(show_missing=True, coverdir="/tmp")
