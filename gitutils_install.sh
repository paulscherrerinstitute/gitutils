#!/bin/bash
echo "Copying the python script to a cli format without .py extension..."
cp ./gitutils/gitutils.py ./gitutils/gitutils
echo "Making it executable..."
chmod +x ./gitutils/gitutils
echo "Adding gitutils folder to the PATH environment variable in the ~/.bash_profile file..."
FILE=~/.bash_profile
if [[ -f "$FILE" ]]; then
    echo $"export PATH=\$PATH:$(pwd)/gitutils" >> $FILE
    source ~/.bash_profile
else
    echo "The ~/.bash_profile was not found. Please, add gitutils folder to the PATH manually in order to use it as a command."
fi