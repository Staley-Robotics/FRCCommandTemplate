#!/bin/bash

# To use this file, run "./setup.sh" in the terminal and follow the instructions

# coloring setup
col_print () {
  echo -e "$2$1\033[0m"
}
GREEN_BOLD="\033[1;32m"
GREEN="\033[32m"
WARNING="\033[1;91m"
ALERT="\033[1;93m"

col_print "\nWelcome to the falcon setup wizard!" $GREEN_BOLD
echo -e "This program will:\n\t - create a python virtual environment\n\t - install pip requirements\n\t - run robotpy sync\nIt will require internet access."
read -p "Proceed? [y/n]: " proceed
if [[ ! "$proceed" =~ ^[yY](es)?$ ]]; then
   col_print "\nExiting." $ALERT
   exit
fi


# '''-------------------Virtual Environment-------------------'''
echo -e "\nChecking for Python Virtual Environment..."

if [[ -n "$VIRTUAL_ENV" ]]; then
  echo -e "\nVirtual environment '$VIRTUAL_ENV' detected as active."
elif [[ -d ".venv" ]]; then
  echo -e "\nVirtual environment '.venv' detected in workspace but not active, activating..."
  source .venv/bin/activate
else
  echo -e "\nNo virtual environment is currently active or detected, creating and activating..."
  col_print "If using VSCode, you should recieve a popup asking if you want to add the python virtual environment to the workplace. Please click yes on this popup." $ALERT
  read -p "Confirm: "
  python3 -m venv .venv
  source .venv/bin/activate
fi


# '''-------------------pip install-------------------'''
echo "Installing project requirements..."
if [[ -f "requirements.txt" ]]; then
  echo -e "\nrequirements.txt detected\n"
  pip install -r requirements.txt
  if [[ "$OSTYPE" == "darwin"* ]]; then
    pip install certifi
  fi
else
  col_print "\nProject requirements file (requirements.txt) not detected. Please find it!" $ALERT
  exit 1
fi


# '''-------------------robotpy-------------------'''
if [[ "$OSTYPE" == "darwin"* ]]; then
    robotpy sync --use-certifi
else
    robotpy sync
fi

col_print "\nEnvironment succesfully setup!" $GREEN_BOLD