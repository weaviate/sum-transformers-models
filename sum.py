from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from pydantic import BaseModel
import torch

class SumInput(BaseModel):
    text: str

class Sum:
    model: AutoModelForSeq2SeqLM
    tokenizer: AutoTokenizer
    cuda: bool
    cuda_core: str

    def __init__(self, model_path: str, cuda_support: bool, cuda_core: str):
        self.cuda = cuda_support
        self.cuda_core = cuda_core
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        device = -1
        if self.cuda:
            self.model.to(self.cuda_core)
            device = int(cuda_core[5:]) # form is e.g. cuda:3
        self.model.eval() # make sure we're in inference mode, not training

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        self.nlp = pipeline("summarization", model=self.model, tokenizer=self.tokenizer, device=device)


    async def do(self, input: SumInput):
        text = input.text
        if len(text) == 0:
            return None
        
        sum_results = self.nlp(text)

        '''
        this is how it looks like:
        sum_results = [{
            "summary_text": "The Eiffel Tower is a landmark in Paris, France."
        }]

        this is how it should look:
        sum_results = [{
            "result": "The Eiffel Tower is a landmark in Paris, France."
        }]
        '''
        
        for item in sum_results:
            item['result'] = item.pop('summary_text')

        return sum_results