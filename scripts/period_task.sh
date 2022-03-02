#!/bin/bash

# Load crontab env from dump file
source /crontab_env

echo "/opt/gitlab-sync/gitlab-sync \
    --local $LOCAL_GTILAB_URL \
    --local-token $LOCAL_GITLAB_TOKEN \
    --local-group $LOCAL_GITLAB_GROUP \
    --remote $REMOTE_GTILAB_URL \
    --remote-token $REMOTE_GTILAB_TOKEN \
    --push-url $REMOTE_GTILAB_PUSH_URL \
    --ignore-branches $IGNORE_BRANCHES \
    --allow-branches $ALLOW_BRANCHES \
    --force-push"

/opt/gitlab-sync/gitlab-sync \
    --debug \
    --verbose \
    --local $LOCAL_GTILAB_URL \
    --local-token $LOCAL_GITLAB_TOKEN \
    --local-group $LOCAL_GITLAB_GROUP \
    --remote $REMOTE_GTILAB_URL \
    --remote-token $REMOTE_GTILAB_TOKEN \
    --push-url $REMOTE_GTILAB_PUSH_URL \
    --ignore-branches $IGNORE_BRANCHES \
    --allow-branches $ALLOW_BRANCHES \
    --force-push
