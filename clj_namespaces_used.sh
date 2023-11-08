#!/usr/bin/env bash

clj-kondo --lint src --config '{:output {:analysis true :format :json}}' | jq -r '.analysis."namespace-usages"[].to' | sort | uniq
