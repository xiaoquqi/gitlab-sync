import urllib.parse

import git

# Default ssh options
SSH_CMD = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

# Ignore remote refs to get real branches
IGNORE_REFS = ["HEAD"]

class GitRepo(object):

    def __init__(self, git_url, src_path):
        self.git_url = urllib.parse.quote(git_url, safe=':/')
        self.src_path = src_path
        self._repo = None

    @property
    def repo(self):
        if not self._repo:
            self._repo = git.Repo(self.src_path)

        return self._repo

    @property
    def branches(self):
        branches = []
        for r in self.repo.remote().refs:
            ref = r.remote_head
            if ref not in IGNORE_REFS:
                branches.append(ref)

        return branches

    @property
    def current_branch(self):
        return self.repo.active_branch.name

    def clone(self):
        git.Repo.clone_from(self.git_url, to_path=self.src_path,
                            env={'GIT_SSH_COMMAND': SSH_CMD})

    def pull_branch(self, remote_branch, local_branch=None):
        if not local_branch:
            local_branch = remote_branch
        self.repo.git.fetch(self.git_url, "%s:%s" % (
            remote_branch, local_branch))

    def push_all_branches(self, force=False):
        self.repo.git.push(self.git_url, "--all", force=force)

    def push_all_tags(self, force=False):
        self.repo.git.push(self.git_url, "--tags", force=force)
