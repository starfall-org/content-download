#!/usr/bin/bash

git config --global user.email "tonglanhchua@gmail.com"
git config --global user.name "TLC"
git add *
GIT_COMMIT_MESSAGE="UPDATE"
GIT_USERNAME="mymaking"
GIT_PASSWORD=$GH_TOKEN
git commit -a -m "$GIT_COMMIT_MESSAGE"

expect -c "
spawn git pull
expect \"Username for 'https://github.com': \"
send \"$GIT_USERNAME\r\"
expect \"Password for 'https://$GIT_USERNAME@github.com': \"
send \"$GIT_PASSWORD\r\"
interact
"