#!/usr/bin/env bash

git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames
