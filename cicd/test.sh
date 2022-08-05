#!/usr/bin/env bash

set -e

local_repo=${LOCAL_REPO?Variable LOCAL_REPO is required}
model_tag=${MODEL_TAG_NAME?Variable MODEL_TAG_NAME is required}

pip3 install -r requirements-test.txt

docker run -d -it -p "8006:8080" "$local_repo":"$model_tag"

python3 test/smoke_test_$model_tag.py