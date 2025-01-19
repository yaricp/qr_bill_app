#!/bin/bash

# check path to folders
mkdir -p /backups/local;
mkdir -p /var/log/database_backup/;

touch /var/log/database_backup/backup_db.log;

cd /backups/local;

result_check_git_init=$(git status 2>&1);
echo "Result_check_git_init = $result_check_git_init";

if [[ $result_check_git_init == "fatal: not a git repository (or any of the parent directories): .git" ]]; then
  git init;
  git config --global user.email "yaricp@gmail.com";
  git config --global user.name "Iaroslav Pisarev";
fi

# backup database
docker exec -i pg pg_dump -U $POSTGRES_USER $POSTGRES_DB > /backups/local/dump.sql

cd /backups/local
git add .
result=$(git status 2>&1)
echo "Result = $result"
if [[ $result != *"nothing to commit"* ]]; then
  echo "Commit"
  git commit -am "backup `date +%d-%m-%Y"_"%H_%M_%S`"
fi
echo "Nothing to commit"
exit 0


