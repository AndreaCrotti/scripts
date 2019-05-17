#!/usr/bin/env bash
set -ex

TOPIC=$1
INPUT_MESSAGE=$2

kafka-avro-console-producer --broker-list kafka.service.consul:29092 \
                            --property schema.registry.url=http://localhost:28081 \
                            --property value.schema="$(cat ~/src/avro-schemas/schemas/loan-settled.json)" \
                            --topic $TOPIC < $INPUT_MESSAGE
