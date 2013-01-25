import sys
# simple script to create a new story

from pyvotal import PTracker
from pyvotal.stories import Story

WAZ = 261683

ptracker = PTracker(user=sys.argv[1], password=sys.argv[2])

project = ptracker.projects.get(WAZ)

story = projects.stories.get(1232)
story.estimate = 3
story.save()
