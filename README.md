# Ask Serverlessland domain specific GenAI chat-bot using serverless and Amazon Bedrock

This sample domeonstrates how to build a domain specific chatbot using serverless and Bedrock. The chatbot employs Retrieval-Augments Generation (RAG) and chat history to provide context for the LLM to answer.

## Services Used
- Amazon API Gateway
- Amazon Kendra
- AWS Lambda
- AWS Step Functions

## Prerequisites
Kendra index. This current implementation uses Amazon Kendra to provide the