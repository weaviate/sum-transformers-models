#!/usr/bin/env bash

set -e

local_repo=${LOCAL_REPO?Variable LOCAL_REPO is required}
model_name=${MODEL_NAME?Variable MODEL_NAME is required}
model_tag=${MODEL_TAG_NAME?Variable MODEL_TAG_NAME is required}

docker build --build-arg "MODEL_NAME=$model_name" -t "$local_repo":"$model_tag" .