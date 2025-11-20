# Environment Setup

## Table of Contents
- [Environment Setup](#environment-setup)
   - [Access the VSCode URL](#access-the-vscode-url)
   - [Installing Solace Agent Mesh](#installing-solace-agent-mesh)
   - [Configuring Solace Agent Mesh](#configuring-solace-agent-mesh)
   - [Optional: Adding prompts to SAM](#optional-adding-prompts)
   - [Next Steps](#next-steps)

## Access the VSCode URL
1. Navigate to the AWS Console

   ![AWS Console](img/access_console.png)

1. Access the Cloudformation Service

   ![CF Console](img/aws_cf.png)

1. Click on the VsCode Stack

   ![CF VSCode](img/vscode_cf.png)

1. Look for the CloudFormation stack outputs section

   ![CF Output](img/vscode_url.png)

1. Open the VsCode in a new tab

   ![VSCode](img/vscode_env.png)


## Installing Solace Agent Mesh

1. Navigate to the sam directory and create a virtual environment
   ```
   cd sam
   python3 -m venv .venv
   ```
1. Activate the virtual environment
   ```
   source .venv/bin/activate
   ```
1. Install the requirements
   ```
   pip install -r requirements.tx
   ```
   > [!IMPORTANT]
   > Make sure you have activated your virtual environment before proceeding with the workshop. Run `source .venv/bin/activate` if you haven't already done so. Anytime you open a new terminal, you will have to navigate to the `sam` dir and activate the python virtual environment

1. Initialize the solace agent mesh
   ```
   sam init --skip
   ```
After initializing sam, you should now see a 
   ```
   .
   ├── configs
   │   ├── agents
   │   │   └── main_orchestrator.yaml
   │   ├── gateways
   │   │   └── webui.yaml
   │   ├── logging_config.yaml
   │   └── shared_config.yaml
   ├── requirements.txt
   └── src
      └── __init__.py
   5 directories, 6 files
   ```

## Configuring Solace Agent Mesh

1. Modify the .env to look like this
   ```
   NAMESPACE="faa/"
   SOLACE_BROKER_URL="ws://<solace_ec2_endpoint>:8008" # e.g. ws://ec2-35-90-45-100.us-west-2.compute.amazonaws.com:8008
   SOLACE_BROKER_VPN="default"
   SOLACE_BROKER_USERNAME="default"
   SOLACE_BROKER_PASSWORD="default"
   SOLACE_DEV_MODE="false"
   SESSION_SECRET_KEY="supersecretpassword"
   FASTAPI_HOST="0.0.0.0"
   FASTAPI_PORT="8000"
   FASTAPI_HTTPS_PORT="8443"
   SSL_KEYFILE=""
   SSL_CERTFILE=""
   SSL_KEYFILE_PASSWORD=""
   ENABLE_EMBED_RESOLUTION="True"
   LOGGING_CONFIG_PATH="configs/logging_config.ini"
   S3_BUCKET_NAME=""
   S3_ENDPOINT_URL=""
   S3_REGION="us-west-2"

   ## AWS Bedrock Configuration
   AWS_ACCESS_KEY_ID="<insert_here>"
   AWS_SECRET_ACCESS_KEY="<insert_here>"
   AWS_SESSION_TOKEN="<insert_here>"
   BEDROCK_MODEL_NAME="bedrock/anthropic.claude-sonnet-4-20250514-v1:0"
   BEDROCK_MODEL_ID="<model_arn>"
   ```

1. Update the necessary variables as follows:
   - `SOLACE_BROKER_URL` - Get the url from the cloud formation output
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` 

      ![Cress Get](img/aws_account_access_creds.png)

      ![Cress Cops](img/aws_account_copy_creds.png)

   - `BEDROCK_MODEL_ID`

      1. Navigate to the Bedrock Service
      ![Bedreock Service](img/bedrock_service.png)

      1. Click on `Cross-region inference` from the Infer menu    
      ![Infer](img/infer.png)

      1. Search for `claude-sonnet-4` under Inference profile
      ![Claude-infer](img/claude-infer.png)

      1. Copy the _Inference profile ARN_ for the _Global Claude Sonnet 4.5_ model
      ![Claude-ARN](img/arn.png)
      
      1. Click the copy to clipboard icon    
      ![ARN Copy](img/arn_copy.png)

1. Save the `.env` file

1. From terminal, run sam `sam run`

1. Navigate to the sam web UI. Note you can get the URL from the cloudformation output

## [Optional] Adding prompts to SAM

## Next Steps
Now you can follow the workshop parts in order, starting with [Part 1: Standard Operating Procedures](100-SOPs.md)
