#!/usr/bin/env python

# https://docs.mistral.ai/platform/client/#embeddings

import os

from mistralai.client import MistralClient

def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = MistralClient(api_key=api_key)

    embeddings_batch_response = client.embeddings(
        model="mistral-embed",
        input=["Embed this sentence.", "As well as this one."],
    )


if __name__ == "__main__":
    main()
