#!/usr/bin/env bash

set -e

local_repo=${LOCAL_REPO?Variable LOCAL_REPO is required}
model_name=${MODEL_NAME?Variable MODEL_NAME is required}
model_tag=${MODEL_TAG_NAME?Variable MODEL_TAG_NAME is required}
onnx_runtime=${ONNX_RUNTIME:=false}
onnx_cpu=${ONNX_CPU:=AVX512_VNNI}

docker build --build-arg "MODEL_NAME=$model_name" --build-arg "ONNX_RUNTIME=$onnx_runtime" --build-arg "ONNX_CPU=$onnx_cpu" -t "$local_repo":"$model_tag" .