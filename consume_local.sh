#!/usr/bin/env bash

OUT=messages.txt
TOPIC=$1

echo "Consuming topic $TOPIC and writing out to $OUT"

kafka-avro-console-consumer --bootstrap-server kafka.service.consul:29092 \
                            --topic $TOPIC \
                            --property schema.registry.url=http://schema-registry:28081 \
                            --from-beginning > $OUT

