#!/usr/bin/env bash
cat definitions.json | jq -r '.transport[].translation_key'