# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3
import os
from typing import List, Dict, Any

# Initializing clients with environment variables
kendra_client = boto3.client('kendra')
bedrock_client = boto3.client('bedrock-runtime')
api_gateway_endpoint_url = os.getenv('API_GATEWAY_ENDPOINT_URL')
apigatewaymanagementapi_client = boto3.client('apigatewaymanagementapi', endpoint_url=api_gateway_endpoint_url)

def handler(event: List[Dict[str, Any]], context: Any) -> str:
    full_response = ""
    model_id = os.getenv('BEDROCK_MODEL_ID')
    anthropic_version = os.getenv('ANTHROPIC_VERSION')
    max_tokens = os.getenv('MAX_TOKENS')

    kendra_results = event["contentResults"][1]['ResultItems']
    kendra_context = process_kendra_results(kendra_results)

    history = get_history_from_records(event["contentResults"][0]['Items'])
    question = event['data']['message']
    connection_id = event['ConnectionID']

    body = json.dumps({
        "anthropic_version": anthropic_version,
        "max_tokens": int(max_tokens),
        "system": generate_system_prompt(kendra_context, history),
        "messages": [{"role": "user", "content": question}]
    })

    response = bedrock_client.invoke_model_with_response_stream(body=body, modelId=model_id)
    full_response = process_response(response, connection_id, full_response)

    return full_response

def process_response(response: Dict[str, Any], connection_id: str, full_response: str) -> str:
    for event in response.get("body"):
        chunk = json.loads(event["chunk"]["bytes"])

        if chunk['type'] == 'message_delta':
            apigatewaymanagementapi_client.post_to_connection(Data="[[END]]", ConnectionId=connection_id)

        if chunk['type'] == 'content_block_delta' and chunk['delta']['type'] == 'text_delta':
            apigatewaymanagementapi_client.post_to_connection(Data=chunk['delta']['text'], ConnectionId=connection_id)
            full_response += chunk['delta']['text']
    return full_response

def generate_system_prompt(docs: List[Dict[str, Any]], history: List[Dict[str, str]]) -> str:
    system_prompt = "For this query, please prioritize the context I will give and try to ground your response as much as possible in just that information including links where possible. Minimizing pulling from other background knowledge unless absolutely necessary. The context provided will be in the form of docs provided on the topic and a history of question and answers. If you don't know the answer, say 'I'm sorry, I don't know'. Return all answers in markdown."

    if docs:
        system_prompt += "\n\n<docs>\n"
        for doc in docs:
            system_prompt += f"<doc>\n<title>{doc['title']}</title>\n<content>{doc['content']}</content>\n<link>{doc['link']}</link>\n</doc>"
        system_prompt += "\n<docs>"

    if history:
        system_prompt += "\n\n<history>\n"
        for h in history:
            system_prompt += f"<item>\n<question>{h['question']}</question>\n<answer>{h['answer']}</answer>\n</item>"
        system_prompt += "\n<history>"

    return system_prompt

def get_history_from_records(records: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    history = []
    for record in records:
        question = record["question"]["S"]
        answer = record["answer"]["S"]
        history.append({"question": question, "answer": answer})
    return history

def process_kendra_results(results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    processed_results = []
    for item in results:
        result = {
            'id': item['Id'],  
            'title': item.get('DocumentTitle', {}).get('Text', ''),
            'content': item.get('DocumentExcerpt', {}).get('Text', ''),
            'link': item.get('DocumentURI', '')
        }
        processed_results.append(result)
    return processed_results
