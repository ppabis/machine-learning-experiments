#!/bin/bash

################################################
# Generates tokenized URL for a given notebook #
# and opens it in a browser if possible.       #
################################################

URL=$(aws sagemaker create-presigned-notebook-instance-url\
 --notebook-instance-name "$1"\
 --region us-east-2\
 --query AuthorizedUrl\
 --output text)

if [[ $(uname) == "Darwin" ]]; then
    open $URL
elif which xdg-open; then
    xdg-open $URL
elif which firefox; then
    firefox $URL
else
    echo "$URL"
fi