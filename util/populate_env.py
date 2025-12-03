#!/usr/bin/env python3
"""
Script to populate .env file with configuration values and retrieve AWS CloudFormation stack outputs.
"""

import os
import subprocess
import json
import sys


def execute_aws_command(command, parse_json=True):
    """
    Execute an AWS CLI command and return the output.
    
    Args:
        command (str): The AWS CLI command to execute
        parse_json (bool): Whether to parse output as JSON (default: True)
        
    Returns:
        dict/str: Parsed JSON output or text output from the command, or None if command fails
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if parse_json:
            return json.loads(result.stdout)
        else:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from command: {command}")
        print(f"Error: {e}")
        return None


def extract_value_from_outputs(outputs, key):
    """
    Extract a value from CloudFormation outputs by key.
    
    Args:
        outputs (list): List of CloudFormation output dictionaries
        key (str): The OutputKey to search for
        
    Returns:
        str: The OutputValue if found, None otherwise
    """
    if not outputs:
        return None
    
    for output in outputs:
        if output.get('OutputKey') == key:
            return output.get('OutputValue')
    return None


def write_env_file(solace_ec2_endpoint=None, documentDB_host=None, qdrant_url=None, api_key=None, aws_account_id=None):
    """
    Write the .env file with configuration values.
    
    Args:
        solace_ec2_endpoint (str): Solace broker endpoint (without protocol and port)
        documentDB_host (str): DocumentDB host endpoint
        qdrant_url (str): Qdrant vector database URL
        api_key (str): Qdrant API key
        aws_account_id (str): AWS Account ID
    """
    # Use provided values or placeholders
    solace_endpoint = solace_ec2_endpoint or "<solace_ec2_endpoint>"
    docdb_host = documentDB_host or "<documentDB_host>"
    qdrant_endpoint = qdrant_url or "<qdrant_url>"
    qdrant_api_key = api_key or "<API_KEY>"
    account_id = aws_account_id or "{AWS_ACCOUNT_ID}"
    
    env_content = f'''NAMESPACE="faa/"
SOLACE_BROKER_URL="ws://{solace_endpoint}:8008"
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
S3_BUCKET_NAME=""
S3_ENDPOINT_URL=""
S3_REGION="us-west-2"
SAM_DOCUMENTDB_MONGO_HOST="{docdb_host}"
SAM_DOCUMENTDB_MONGO_PORT="27017"
SAM_DOCUMENTDB_MONGO_USER="faa"
SAM_DOCUMENTDB_MONGO_PASSWORD="faaistheb3st"
SAM_DOCUMENTDB_MONGO_DB="FAAData"

## FDPS Position Collection
FLIGHT_DB_MONGO_COLLECTION="FDPSPosition"
FLIGHT_DB_DB_PURPOSE="this database includes information about enroute flights including location, speed, and altitude"
FLIGHT_DB_DB_DESCRIPTION="data includes which artcc center the aircraft is in, the departure and arrival information along with its current enroute position (latitude, longitude), actual speed (KNOTS), altitude along with the flight number (AircractIdentification) and flight plan id."

## STDDS Position Collection
SAM_DOCUMENTDB_STDDS_COLLECTION="STDDSPosition"
SAM_DOCUMENTDB_STDDS_DB_PURPOSE="this database includes information about flight surface data"
SAM_DOCUMENTDB_STDDS_DB_DESCRIPTION="The STDDS database contains real-time FAA flight tracking records that capture comprehensive aircraft operational data including precise GPS coordinates, altitude, speed, velocity vectors, flight identification details, route information, departure and arrival airports, runway usage times, ADS-B surveillance broadcasts, and current flight status, providing a complete situational awareness picture for air traffic management, surface movement monitoring, and aviation safety analysis across the national airspace system."

## Flight Plan Collection
SAM_DOCUMENTDB_FLIGHTPLAN_COLLECTION="FDPSFlightPlan"
SAM_DOCUMENTDB_FLIGHTPLAN_DB_PURPOSE="this database includes information about filed flight plans"
SAM_DOCUMENTDB_FLIGHTPLAN_DB_DESCRIPTION="Contains real-time flight plan records from the FAA's Flight Data Processing System (FDPS) with comprehensive aircraft information, routing details, equipment capabilities, ATC coordination data, and flight status tracking for both commercial and general aviation operations across the National Airspace System."

## Qdrant Configuration
QDRANT_URL="{qdrant_endpoint}:6333"
QDRANT_API_KEY="{qdrant_api_key}"
QDRANT_COLLECTION="SOP-{account_id}"
QDRANT_EMBEDDING_DIMENSION=1024
OPENAI_EMBEDDING_MODEL="text-embedding-ada-002"
DOCUMENTS_PATH="sop"

## AWS Bedrock Configuration
AWS_ACCESS_KEY_ID="<insert_here>"
AWS_SECRET_ACCESS_KEY="<insert_here>"
AWS_SESSION_TOKEN="<insert_here>"
BEDROCK_MODEL_NAME="bedrock/anthropic.claude-sonnet-4-20250514-v1:0"
BEDROCK_MODEL_ID="arn:aws:bedrock:us-west-2:{account_id}:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0"
BEDROCK_EMBEDDING_MODEL_NAME="bedrock/amazon.titan-embed-text-v2:0"
'''
    
    env_file_path = ".env"
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"Successfully wrote .env file to: {os.path.abspath(env_file_path)}")
        return True
    except Exception as e:
        print(f"Error writing .env file: {e}")
        return False


def main():
    """
    Main function to orchestrate CloudFormation stack retrieval and .env file creation.
    """
    
    # Get AWS Account ID
    # print("Retrieving AWS Account ID...")
    aws_account_id = execute_aws_command(
        "aws sts get-caller-identity --query 'Account' --output text",
        parse_json=False
    )
    
    
    # Execute CloudFormation commands
    # print("Step 2: Retrieving CloudFormation stack outputs...")
    # print()
    
    # print("Retrieving vscode stack outputs...")
    vscode_cf_output = execute_aws_command(
        "aws cloudformation describe-stacks --stack-name vscode --query 'Stacks[0].Outputs'"
    )
    
    # print("Retrieving faa-infrastructure-studio stack outputs...")
    studio_cf_output = execute_aws_command(
        "aws cloudformation describe-stacks --stack-name faa-infrastructure-studio --query 'Stacks[0].Outputs'"
    )
    

    # Extract values from CloudFormation outputs
    # print("Step 3: Extracting configuration values...")
    
    solace_ec2_endpoint = None
    documentDB_host = None
    qdrant_url = None
    api_key = None
    
    if studio_cf_output:
        # Extract SolaceBrokerEndpoint and remove http:// and :8080
        solace_broker_full = extract_value_from_outputs(studio_cf_output, 'SolaceBrokerEndpoint')
        if solace_broker_full:
            # Remove http:// or https:// prefix
            solace_ec2_endpoint = solace_broker_full.replace('http://', '').replace('https://', '')
            # Remove port if present
            if ':' in solace_ec2_endpoint:
                solace_ec2_endpoint = solace_ec2_endpoint.split(':')[0]
            # print(f"  Solace EC2 Endpoint: {solace_ec2_endpoint}")
        
        # Extract DocumentDB endpoint
        documentDB_host = extract_value_from_outputs(studio_cf_output, 'DocumentDBEndpoint')
        # if documentDB_host:
            # print(f"  DocumentDB Host: {documentDB_host}")
        
        # Extract Qdrant URL
        qdrant_url = extract_value_from_outputs(studio_cf_output, 'VectorDBEndpoint')
        # if qdrant_url:
        #     print(f"  Qdrant URL: {qdrant_url}")
        
        # Extract Qdrant API Key
        api_key = extract_value_from_outputs(studio_cf_output, 'VectorDBKey')
    #     if api_key:
    #         print(f"  Qdrant API Key: {api_key[:20]}...")
    # print()
    
    # Write .env file with extracted values
    # print("Step 4: Writing .env file...")
    if not write_env_file(solace_ec2_endpoint, documentDB_host, qdrant_url, api_key, aws_account_id):
        print("Failed to write .env file. Exiting.")
        sys.exit(1)
    # print()
    
    # Summary
    # print("=" * 60)
    # print("Summary:")
    # print("=" * 60)
    # print(f".env file created: {os.path.abspath('.env')}")
    # print(f"VSCode stack outputs retrieved: {'Yes' if vscode_cf_output else 'No'}")
    # print(f"Studio stack outputs retrieved: {'Yes' if studio_cf_output else 'No'}")
    # print()
    if solace_ec2_endpoint and documentDB_host and qdrant_url and api_key and aws_account_id:
        print("✓ All configuration values successfully extracted and populated")
    else:
        print("⚠ Some configuration values could not be extracted")
        if not aws_account_id:
            print("  - AWS Account ID: Missing")
        if not solace_ec2_endpoint:
            print("  - Solace EC2 Endpoint: Missing")
        if not documentDB_host:
            print("  - DocumentDB Host: Missing")
        if not qdrant_url:
            print("  - Qdrant URL: Missing")
        if not api_key:
            print("  - Qdrant API Key: Missing")
        print("  Please review the .env file and replace any remaining placeholders")
    print()
    print("Next steps:")
    print("1. Review the .env file at: .env")
    print("2. Add your AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)")
    print("=" * 60)


if __name__ == "__main__":
    main()