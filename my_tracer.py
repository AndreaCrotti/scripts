import sys

# from http://www.doughellmann.com/PyMOTW/sys/tracing.html
# use it as a base to get something smarter

def trace_lines(frame, event, arg):
    if event != 'line':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename
    line_text = open(filename).readlines()[line_no-1].strip()
    print '  %s line %s, %s' % (func_name, line_no, line_text)

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    line_no = frame.f_lineno
    filename = co.co_filename
    print 'Call to %s on line %s of %s' % (func_name, line_no, filename)
    if func_name in TRACE_INTO:
        # Trace into this function
        return trace_lines
    return

def c(input):
    print 'input =', input
    print 'Leaving c()'

def b(arg):
    val = arg * 5
    c(val)
    print 'Leaving b()'

def a():
    b(2)
    print 'Leaving a()'
    
TRACE_INTO = ['b']

sys.settrace(trace_calls)
a()
