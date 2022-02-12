# About

This script is used to sync between gitlab in group level, including all subgroups and projects.

# How to use?

## Command Help

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

## Use Docker to run

```
docker run \
  --rm -it \
  -v $HOME:/root \
  --name gitlab-sync \
  gitlab-sync:latest \
  gitlab-sync \
    --local http://192.168.10.254:20080 \
    --local-token hyZ3ay3kt3zWvLMx2LGP \
    --local-group hypermotion \
    --remote http://gitlab.oneprocloud.com:31080 \
    --remote-token eWyUea2qLpA6byv5SpB1 \
    --remote-group hypermotion \
    --push-url ssh://git@gitlab.oneprocloud.com:31022
```
