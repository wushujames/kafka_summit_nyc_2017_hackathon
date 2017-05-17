#!/usr/bin/python

import sys
import json

print "digraph {"

topics = set()
for line in sys.stdin:
    line = line.strip()
    (client, verb, topic) = line.split()
    if client.endswith('-producer'):
        client = client[:-len('-producer')]
    if client.endswith('-consumer'):
        client = client[:-len('-consumer')]
    if topic not in topics:
        print '    %s [label="%s" shape=box]' % (json.dumps(topic), topic)
    if verb == 'producing_to':
        print '    %s -> %s' % (json.dumps(client), json.dumps(topic))
    if verb == 'consuming_from':
        print '    %s -> %s' % (json.dumps(topic), json.dumps(client))

print '}'
