# Domain specific GenAI chat-bot using serverless technologies and Amazon Bedrock

This sample demonstrates how to build a domain specific chatbot using serverless and Bedrock. The chatbot employs Retrieval-Augments Generation (RAG) and chat history to provide context for the LLM to answer. 

***Caution: deploying and running this application can incur charges on AWS. All services used offer a free tier to get started but please be aware.***

## Services Used
- Amazon API Gateway
- Amazon Kendra
- AWS Lambda
- AWS Step Functions
- Amazon Bedrock (Model: Anthropic Claude v3 Sonnet)

## Prerequisites
* An active [AWS](https://aws.amazon.com) account with administrative permissions
* **Kendra index**: This implementation uses [Amazon Kendra](https://aws.amazon.com/kendra/) to provide the retrieval augmented generation (RAG) functionality. Create any kind of index you want. Once the index is populated, obtain the index ID for use during deployment. *Please note, Amazon Kendra incurs charges to use.*
* [AWS CLI](https://aws.amazon.com/cli/) installed and configured.
* [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed and configured.
* [Docker](https://www.docker.com/) installed and configured.

## Installing
1. Run the following from the root of the project
1. Build the application and prepare for deployment using AWS SAM. We are using containers so you don't have to setup the development environment. The application uses Python 3.12.
    ```
    sam build --use-container
    ```
1. Deploy the application AWS SAM
    ```
    sam deploy -g
    ```
    * Accept the default or enter the desired **Stack Name**:
    * Accept the default or enter the desired **AWS Region**:
    * Accept the default or enter the desired **ApiStageName**:
    * Enter your **KendraIndex**:
    * Accept the default or enter the desired **BedrockModel**: (*Note: This application and prompt format is specific to Claude 3 (any variant)*)
    * Accept the default or enter the desired **AnthropicVersion**
    * **Accept all defaults from here on out**

## Testing
1. Obtain your websocket endpoint from the output of the deployment.
1. Using your favorite websocket client, connect to the wss endpoint.
1. Send your message in the following format:
    ```
    {"message":"Your question here"}
    ```

## Cleanup
From the root of the project, run the following command:
```
sam delete --stack-name <your stack name>
```
Accept the defaults.