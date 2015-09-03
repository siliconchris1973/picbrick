#!/usr/bin/env sh

ENV_FILE="env/environment"

if [ -f "$ENV_FILE" ]
then
    source $ENV_FILE
    echo "environment setup, starting picbrick.py"
    env smsHash=$smsHash ./picbrick.py
else
    echo "ATTENTION! The environment file $ENV_FILE is not present."
    echo "This file is used to setup the environment of picbrick. "
    echo "it contains shell environment variables, such as the hash key"
    echo "for the sms service, that are not uploaded to github."
    echo "If you do not want to use this file to setup the environment,"
    echo "but rather set the environment by other means, then you can "
    echo "simply start picbrick via "
    echo "      sudo ./picbrick.py"
    echo "and savely ignore this little shell-script"
    echo "Otherwise take a look at the README.md file on how to create "
    echo "the file with the necessary environment variables"
fi
