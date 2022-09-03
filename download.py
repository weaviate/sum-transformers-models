#!/usr/bin/env python3

import os
import sys
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = os.getenv('MODEL_NAME') #google/pegasus-xsum
if model_name is None or model_name == "":
    logging.error("Fatal: MODEL_NAME is required")
    sys.exit(1)

logging.info(f"Downloading model ${model_name} from huggingface model hub")

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

model.save_pretrained('./models/model')
tokenizer.save_pretrained('./models/model')