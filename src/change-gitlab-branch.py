import gitlab

# GitLab实例URL和访问令牌
GITLAB_URL = 'https://your.gitlab.instance.com'
GITLAB_TOKEN = 'your-gitlab-access-token'

# 要修改的组ID和保护分支设置
GROUP_ID = 123
PROTECTED_BRANCH_SETTINGS = {
    'name': 'master',
    'push_access_level': gitlab.DEVELOPER_ACCESS,
    'merge_access_level': gitlab.DEVELOPER_ACCESS,
    'unprotect_access_level': gitlab.DEVELOPER_ACCESS,
}

# 连接到GitLab API
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

# 获取指定组下的所有项目
group = gl.groups.get(GROUP_ID)
projects = group.projects.list(all=True)

# 针对每个项目，修改其保护分支设置
for project in projects:
    print(f'Modifying protected branch settings for project "{project.name}"...')
    try:
        branch = project.protectedbranches.get(PROTECTED_BRANCH_SETTINGS['name'])
        branch.push_access_level = PROTECTED_BRANCH_SETTINGS['push_access_level']
        branch.merge_access_level = PROTECTED_BRANCH_SETTINGS['merge_access_level']
        branch.unprotect_access_level = PROTECTED_BRANCH_SETTINGS['unprotect_access_level']
        branch.save()
        print(f'Successfully modified protected branch settings for project "{project.name}".')
    except gitlab.exceptions.GitlabGetError:
        print(f'Protected branch "{PROTECTED_BRANCH_SETTINGS["name"]}" does not exist in project "{project.name}".')
    except gitlab.exceptions.GitlabUpdateError as e:
        print(f'Failed to modify protected branch settings for project "{project.name}": {e}.')
