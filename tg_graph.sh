#!/usr/bin/env bash

terraform graph | dot -T png -o graph.png && eog graph.png
