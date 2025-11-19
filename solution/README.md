# FAA + SAM working demo

## Prerequisites
1. Python 3.10+
1. AWS Account with resources configured

## Running

1. Create a virtual env
   ```
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

1. Update the env variables in `.env`

1. Run sam
   ```
   sam run
   ```