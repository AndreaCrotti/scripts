#!/usr/bin/env python
"""
Generate the procmail rules
in a more object oriented way

In general procmail rules are in the form
- :0 [flags] [: [lock-file] ]
- zero or more conditions
- one action line
"""

# TODO: always write out the correct path and shell for the user

class Filter(object):
    "Filter generator"
    def __init__(self, actions, conditions, flags = []):
        pass

    def procmail_rule(self):
        "Generate procmail rule"
        pass
    
