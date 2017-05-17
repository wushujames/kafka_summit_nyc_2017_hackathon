#!/usr/bin/python

import sys

file = sys.argv[1]
for line in open(file):
    line = line.strip()
    if 'api_key=0,' in line:
        # Produce request
        parts = line.split()
        producer_info = parts[5].split(':')[1]
        producer_info = producer_info.replace('{', '').replace('}','')
        for part in producer_info.split(','):
            (key, value) = part.split('=')
            if key == 'client_id':
                client_id = value
        topic_data_start = line.find('topic_data=[{')
        topic_part_str = line[topic_data_start + len('topic_data=[{'):]
        topic_kv = topic_part_str[:topic_part_str.find(',')]
        (foo, topic_name) = topic_kv.split('=')
        print '%s producing_to %s' % (client_id, topic_name)
        continue
    if 'api_key=1,' in line: # notice I grep for '1<comma>'. That is so that I don't match api_key=18
        parts = line.split()
        consumer_info = parts[5].split(':')[1]
        consumer_info = consumer_info.replace('{', '').replace('}','')
        for part in consumer_info.split(','):
            (key, value) = part.split('=')
            if key == 'client_id':
                client_id = value
        topic_data_start = line.find('topics=[{')
        topic_part_str = line[topic_data_start + len('topics=[{'):]
        topic_kv = topic_part_str[:topic_part_str.find(',')]
        (foo, topic_name) = topic_kv.split('=')
        print '%s consuming_from %s' % (client_id, topic_name)
        pass
    
    

