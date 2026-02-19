#!/bin/bash
col_print () {
  echo -e "$2$1\033[0m"
}

echo -e "\nWelcome to the terrible setup wizard!"
echo "This will: create a python virtual environment, install pip requirements, and run robotpy sync. It will require internet access. Proceed? [y/n]: "
read proceed
if [[ ! "$proceed" =~ ^[yY](es)?$ ]]; then
   col_print "\nExiting." "\033[31m"
   exit
fi


# '''-------------------Virtual Environment-------------------'''
echo "Checking for Python Virtual Environment..."

if [[ -n "$VIRTUAL_ENV" ]]; then
  echo "Virtual environment '$VIRTUAL_ENV' detected as active."
elif [[ -d ".venv" ]]; then
  echo "Virtual environment '.venv' detected in workspace but not active, activating..."
  source .venv/bin/activate
else
  echo "No virtual environment is currently active, creating and activating..."
  python3 -m venv .venv
  source .venv/bin/activate
fi


# '''-------------------pip install-------------------'''
echo "Installing project requirements..."
if [[ -f "requirements.txt" ]]; then
  echo "requirements.txt detected"
  pip install -r requirements.txt
  if [[ "$OSTYPE" == "darwin"* ]]; then
    pip install certifi
  fi
else
  echo "Project requirements file (requirements.txt) not detected. Please find it!"
  exit 1
fi


# '''-------------------robotpy-------------------'''
if [[ "$OSTYPE" == "darwin"* ]]; then
    robotpy sync --use-certifi
else
    robotpy sync
fi

echo "Environment succesfully setup!"