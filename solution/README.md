# FAA + SAM working demo

## Prerequisites
1. Python 3.10+
1. AWS Account with resources configured

## Running

1. Create a virtual env
   ```
   uv venv --python 3.11
   ```
1. Activate the virtual environment
   ```
   source .venv/bin/activate
   ```
1. Install the requirements
   ```
   uv pip install -r requirements.txt 
   ```

1. Update the env variables in `.env`

1. Run sam
   ```
   sam run
   ```