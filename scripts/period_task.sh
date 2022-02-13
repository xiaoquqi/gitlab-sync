#!/bin/bash

# Load crontab env from dump file
source /crontab_env

echo "/opt/gitlab-sync/gitlab-sync \
    --local $LOCAL_GTILAB_URL \
    --local-token $LOCAL_GITLAB_TOKEN \
    --local-group $LOCAL_GITLAB_GROUP \
    --remote $REMOTE_GTILAB_URL \
    --remote-token $REMOTE_GTILAB_TOKEN \
    --remote-group $REMOTE_GTILAB_GROUP \
    --push-url $REMOTE_GTILAB_PUSH_URL"

/opt/gitlab-sync/gitlab-sync \
    --local $LOCAL_GTILAB_URL \
    --local-token $LOCAL_GITLAB_TOKEN \
    --local-group $LOCAL_GITLAB_GROUP \
    --remote $REMOTE_GTILAB_URL \
    --remote-token $REMOTE_GTILAB_TOKEN \
    --remote-group $REMOTE_GTILAB_GROUP \
    --push-url $REMOTE_GTILAB_PUSH_URL
