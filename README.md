# sum-transformers-models

Transformers-based Summarization inference models based on transformers architecture
## Documentation

Documentation for this module can be found [here](https://weaviate.io/developers/weaviate/current/reader-generator-modules/sum-transformers.html).

## Information

The Summarization module is a Weaviate module that is used to summarize Weaviate text objects at query time.

### Pre-built images

|Model Name|Image Name|
|---|---|
|`facebook-bart-large-cnn` ([Info](https://huggingface.co/facebook/bart-large-cnn))|`semitechnologies/sum-transformers:facebook-bart-large-cnn-1.0.0`|

## Build Docker Container

```sh
LOCAL_REPO="sum-transformers" MODEL_TAG_NAME="facebook-bart-large-cnn" MODEL_NAME="facebook/bart-large-cnn" ./cicd/build.sh
```

# More Information

For more information, visit the [official documentation](https://weaviate.io/developers/weaviate/current/modules/).