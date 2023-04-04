# About

This script is used to sync between gitlab in group level, including all subgroups and projects.

Use the default docker, you can run a schedule job to sync between gitlab.

2023-04-04 UPDATE: By default, sync all local groups to remote and you can save all groups under a remote parent group
UPDATE: Support multiple groups sync and no need to pre-create remote groups.

# How to use script?

## (Recommendation)Run in Docker

If you want to run a schedule job to sync between gitlabs, you can use this docker. By default, the docker use Linux crontab to run period task. Here's the detailed:

### Get code

```
git clone https://github.com/xiaoquqi/gitlab-sync
```

### SSH Keys

By default, ssh key mount dir is under gitlab-sync/conf/ssh, you can copy your existing keys here or generate a new one.

```
cd gitlab-sync
ssh-keygen -t rsa -b 2048 -f conf/ssh/id_rsa -q -N ""
```

Make sure your own key or generated key already uploaded to local and remote gitlab. By default, we will use ssh url to get local code for private repositories.

```
cat conf/ssh/id_rsa.pub
```

* Login your gitlab
* Right Corner and click icon
* Click [Preferences]
* Select [SSH Keys] on the left menu
* Copy and Paste your public key
* Click [Add Keys]

### Modify Environment

Prepare to copy samples to runtime env and configs

```
cp env.sample .env
cp conf/crontab/cron.exmaple crontab/cron
```

Modify your .env and use your gitlab local and remote configurations.

* LOCAL_GTILAB_URL: The gitlab you want set as source
* LOCAL_GITLAB_TOKEN: Token to access your gitlab, we need find out all your groups and projects, all the actions are read
* LOCAL_GITLAB_GROUP: Local gitlab groups you sync to remote, use comma to seperate
* REMOTE_GTILAB_URL: Remote gitlab as target
* REMOTE_GTILAB_TOKEN: Token to access your remote gitlab, we need to read and create groups and projects if not exists
* REMOTE_GTILAB_GROUP: Remote root groups you set as target, use comma to seperate, the total nubmers of groups should equal to local groups
* REMOTE_GTILAB_PUSH_URL: Remote push base url, ex: ssh://git@remote.gitlab.com:ssh_port
* IGNORE_BRANCHES: Branches not sync
* ALLOW_BRANCHES: Branches need to sync, ignore branches's priority is higher than ignore branches
* FORCE_PUSH: If add force when push
* REMOTE_PARENT_GROUP: Sync all projects under this parent group

### Schedule Settings

Modify scheduler settings in the conf/crontab/cron file, this file will mount inside docker after running, here's an exmaple:

You just need to change the crontab scheduler, and ignore the command part. We use flock to lock the task to avoid duplicate running.

```
0 23 * * * /usr/bin/flock -n /tmp/crontab.lockfile bash /period_task.sh >> /var/log/gitlab-sync.log
```

### Volume Mounts

* SSH Keys: By default, we need to use your ssh key to access your gitlab projects. By default, I mount your $HOME/.ssh to /root/.ssh in docker.
* Logs setting: By default, we write the stdout and stderr logs to /var/log/gitlab-sync/gitlab-sync.log and already mount your OS /var/log/gitlab-sync to your host, you can check log from there 

### Run as Daemon

```
docker-compuse up -d
```

## CLI Help

You can also use the script in your own environment, Python 3.6+ and virtualenv are recommended.

```
virtualenv-3 venv3
source venve3/bin/activate
pip install -r src/requirements.txt
```

```
usage: gitlab-sync [-h] --local LOCAL --local-token LOCAL_TOKEN [--local-group LOCAL_GROUP] --remote REMOTE --remote-token REMOTE_TOKEN
                   [--remote-group REMOTE_GROUP] [--remote-parent-group REMOTE_PARENT_GROUP] --push-url PUSH_URL [--force-push]
                   [--ignore-branches IGNORE_BRANCHES] [--allow-branches ALLOW_BRANCHES] [-d] [-v]

Gitlab backup tool in group level

optional arguments:
  -h, --help            show this help message and exit
  --local LOCAL         Local gitlab http url, ex: https://local.gitlab.com
  --local-token LOCAL_TOKEN
                        Local gitlab private token.
  --local-group LOCAL_GROUP
                        Local github group for syncing, Leave this as blank when you want to sync all groups
  --remote REMOTE       Remote gitlab http url, ex: https://remote.gitlab.com
  --remote-token REMOTE_TOKEN
                        Remote gitlab private token
  --remote-group REMOTE_GROUP
                        Target group of remote github for backup, Leave this as blank if you want to keep the same name as remote
  --remote-parent-group REMOTE_PARENT_GROUP
                        Parent group to save all local groups
  --push-url PUSH_URL   Remote push url for backup target
  --force-push          Force push to remote by default
  --ignore-branches IGNORE_BRANCHES
                        Not sync for ignore branches, ex: cherry-pick,dev,temp
  --allow-branches ALLOW_BRANCHES
                        Only sync for allow branches, ex: master,main,qa. if not given, sync all branches. If ignore branches is given,
                        thepriority is higher than this argument
  -d, --debug           Enable debug message.
  -v, --verbose         Show message in standard output.
```

# Gitlab Tips

## Create a personal access token

You can create as many personal access tokens as you like.

1. In the top-right corner, select your avatar.
2. Select Edit profile.
3. On the left sidebar, select Access Tokens.
4. Enter a name and optional expiry date for the token.
5. Select the desired scopes.
6. Select Create personal access token.
7. Save the personal access token somewhere safe. After you leave the page, you no longer have access to the token.
