import os
from logging import getLogger
from fastapi import FastAPI, Response, status
from sum import Sum, SumInput
from meta import Meta

app = FastAPI()
sum : Sum
meta_config : Meta
logger = getLogger('uvicorn')


@app.on_event("startup")
def startup_event():
    global sum
    global meta_config

    cuda_env = os.getenv("ENABLE_CUDA")
    cuda_support=False
    cuda_core=""

    if cuda_env is not None and cuda_env == "true" or cuda_env == "1":
        cuda_support=True
        cuda_core = os.getenv("CUDA_CORE")
        if cuda_core is None or cuda_core == "":
            cuda_core = "cuda:0"
        logger.info(f"CUDA_CORE set to {cuda_core}")
    else:
        logger.info("Running on CPU")

    model_dir = './models/model'
    onnx_runtime = os.path.exists(f"{model_dir}/decoder_model.onnx")
    if onnx_runtime:
        logger.info("Running using ONNX runtime")

    sum = Sum(model_dir, cuda_support, cuda_core, onnx_runtime)
    meta_config = Meta(model_dir)


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    return meta_config.get()


@app.post("/sum")
async def read_item(item: SumInput, response: Response):
    try:
        summary = await sum.do(item)

        jsonToReturn = {
            "text": item.text,
            "summary": summary
        }

        '''
        summary = [{
                "result": "string"
            }] # Or None

        text = "string"
        '''

        return jsonToReturn

    except Exception as e:
        logger.exception(
            'Something went wrong while extracting data.'
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}