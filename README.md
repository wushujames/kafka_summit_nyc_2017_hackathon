First, I turned the debuglog levels up to TRACE. Here is what I did in the broker's log4j config file:
```
log4j.logger.kafka.network.Processor=TRACE, requestAppender
log4j.logger.kafka.server.KafkaApis=TRACE, requestAppender
log4j.additivity.kafka.server.KafkaApis=false
```

The kafka-requests.log file I included here contains only a subset of the lines from my actual kafka-requests.log file.
```
$ grep -E 'api_key=(1,|0)' logs/kafka-request.log.2017-05-07-20  > kafka-requests.log

$ python requests.py kafka-requests.log  | sort | uniq
StreamJobA-StreamThread-1-consumer consuming_from topic1
StreamJobA-StreamThread-1-producer producing_to topic2
StreamJobAClientId-StreamThread-1-consumer consuming_from topic1
StreamJobAClientId-StreamThread-1-producer producing_to topic2
rdkafka consuming_from test
rdkafka consuming_from topic2
rdkafka producing_to test
rdkafka producing_to topic1

$ python requests.py kafka-requests.log  | sort | uniq > requests.in
$ cat requests.in | python to_dot.py
digraph {
    "topic1" [label="topic1" shape=box]
    "topic1" -> "StreamJobA-StreamThread-1"
    "topic2" [label="topic2" shape=box]
    "StreamJobA-StreamThread-1" -> "topic2"
    "topic1" [label="topic1" shape=box]
    "topic1" -> "StreamJobAClientId-StreamThread-1"
    "topic2" [label="topic2" shape=box]
    "StreamJobAClientId-StreamThread-1" -> "topic2"
    "test" [label="test" shape=box]
    "test" -> "rdkafka"
    "test" [label="test" shape=box]
    "rdkafka" -> "test"
    "topic1" [label="topic1" shape=box]
    "rdkafka" -> "topic1"
    "topic2" [label="topic2" shape=box]
    "topic2" -> "reader"
}

$ cat requests.in | python to_dot.py > dataflow.dot

$ dot -Tpng dataflow.dot > dataflow.png

```