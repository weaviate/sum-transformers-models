#!/usr/bin/env python3

import os
import sys
import logging
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from optimum.onnxruntime import ORTModelForSeq2SeqLM

def fix_config_json(model_dir: str, model_name: str):
    with open(f"{model_dir}/config.json", 'r') as f:
        data = json.load(f)

    if model_name == "facebook/bart-large-cnn":
        data["model_type"] = "bart"

    with open(f"{model_dir}/config.json", 'w') as json_file:
        json.dump(data, json_file)

model_dir = './models/model'
model_name = os.getenv('MODEL_NAME')
if model_name is None or model_name == "":
    print("Fatal: MODEL_NAME is required")
    sys.exit(1)

onnx_runtime = os.getenv('ONNX_RUNTIME')
if not onnx_runtime:
    onnx_runtime = "false"

onnx_cpu_arch = os.getenv('ONNX_CPU')
if not onnx_cpu_arch:
    onnx_cpu_arch = "ARM64"

logging.info(f"Downloading model ${model_name} from huggingface model hub")

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(model_dir)

if onnx_runtime.lower() == "true" or onnx_runtime == "1":
    # Download the model
    ort_model = ORTModelForSeq2SeqLM.from_pretrained(model_name, from_transformers=True)
    ort_model.save_pretrained(model_dir)
    fix_config_json(model_dir, model_name)
else:
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.save_pretrained(model_dir)
