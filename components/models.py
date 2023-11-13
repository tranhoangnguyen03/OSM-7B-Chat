
import requests
import json
from pydantic import ValidationError, BaseModel
from typing import List
from loguru import logger

supported_models = {
    'mistralai/Mistral-7B-Instruct-v0.1':'https://colab.research.google.com/drive/1YcLF-03TJmtTp4gPT0aVIKXX8wf0Bvh1',
    'HuggingFaceH4/zephyr-7b-beta':'https://colab.research.google.com/drive/1vIgUmaB4DV21-MNFnRgFlXXWbNmr4b7s',
    'amazon/MistralLite':'https://colab.research.google.com/drive/1RT7Ekl-ZU8O9q2P1eBF1jehl48Lzovni',
    'teknium/OpenHermes-2.5-Mistral-7B':'https://colab.research.google.com/drive/1p1YNtD7NB_Hs2X8PeDDMe_Ji9_rvSndF',
    'ehartford/dolphin-2.2.1-mistral-7b':'https://colab.research.google.com/drive/11-PcgXNPM1sLrvRmeHRemJl9V4mQ09UL',
    'SciPhi/SciPhi-Self-RAG-Mistral-7B-32k':'https://colab.research.google.com/drive/1Q-jNpgvGEzTWvl94AiLZ7tRvbA3E7kwL',
    'Custom Model':'https://colab.research.google.com/drive/1bPzHcUkQbcRINJgiiDanMjP0vFuHtRR5',
}


class ModelData(BaseModel):
    id: str
    object: str
    owned_by: str
    permissions: List  # Assuming permissions is a list of unspecified objects

class ApiResponse(BaseModel):
    object: str
    data: List[ModelData]

def retrieve_model_name(api_endpoint: str) -> ApiResponse:
    logger.debug(api_endpoint)
    response = requests.get(f'{api_endpoint}/models').content

    # Convert byte string to Python dictionary
    response_dict = json.loads(response.decode('utf-8'))

    # Parse the dictionary using the Pydantic model
    try:
        parsed_response = ApiResponse(**response_dict)
        return parsed_response.data[0].id.replace('./models/','').replace('.Q6_K.gguf','')
    except ValidationError as e:
        print("Error in parsing:", e)
        return None