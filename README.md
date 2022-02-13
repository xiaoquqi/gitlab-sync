# About

This script is used to sync between gitlab in group level, including all subgroups and projects.

Use the default docker, you can run a schedule job to sync between gitlab.

# How to use script?

## (Recommendation)Run in Docker

If you want to run a schedule job to sync between gitlabs, you can use this docker. By default, the docker use Linux crontab to run period task. Here's the detailed:

### Modify Environment

Copy env.sample to local default env.

```
cp env.sample .env
```

Modify your .env and use your gitlab local and remote configurations.

* LOCAL_GTILAB_URL: The gitlab you want set as source
* LOCAL_GITLAB_TOKEN: Token to access your gitlab, we need find out all your groups and projects, all the actions are read
* LOCAL_GITLAB_GROUP: Local gitlab group you sync to remote
* REMOTE_GTILAB_URL: Remote gitlab as target
* REMOTE_GTILAB_TOKEN: Token to access your remote gitlab, we need to read and create groups and projects if not exists
* REMOTE_GTILAB_GROUP: Remote root group you set as target
* REMOTE_GTILAB_PUSH_URL: Remote push base url, ex: ssh://git@remote.gitlab.com:ssh_port

### Schedule Settings

Modify scheduler settings in the crontab/cron file, this file will mount inside docker after running, here's an exmaple:

You just need to change the crontab scheduler, and ignore the command part. We use flock to lock the task to avoid duplicate running.

```
0 23 * * * /usr/bin/flock -n /tmp/crontabl.lockfile bash /period_task.sh >> /var/log/gitlab-sync.log
```

### Volume Mounts

By default, we need to use your ssh key to access your gitlab projects. By default, I mount your $HOME/.ssh to /root/.ssh in docker.

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
usage: gitlab-sync.py [-h] --local LOCAL --local-token LOCAL_TOKEN
                      --local-group LOCAL_GROUP --remote REMOTE --remote-token
                      REMOTE_TOKEN --remote-group REMOTE_GROUP --push-url
                      PUSH_URL [-d] [-v]

Gitlab backup tool in group level

optional arguments:
  -h, --help            show this help message and exit
  --local LOCAL         Local gitlab http url, ex: https://local.gitlab.com
  --local-token LOCAL_TOKEN
                        Local gitlab private token.
  --local-group LOCAL_GROUP
                        Local github group for reading.
  --remote REMOTE       Remote gitlab http url, ex: https://remote.gitlab.com
  --remote-token REMOTE_TOKEN
                        Remote gitlab private token
  --remote-group REMOTE_GROUP
                        Target group of remote github for backup.
  --push-url PUSH_URL   Remote push url for backup target
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
