import logging

import gitlab
import requests
from retrying import retry


def retry_if_timeout(exception):
    return isinstance(exception, requests.exceptions.ReadTimeout)


class GitlabWrapper(object):

    def __init__(self, api_url, private_token):
        self.gl = gitlab.Gitlab(
            url=api_url, private_token=private_token)
        self._groups = []

    @property
    def groups(self):
        if not self._groups:
            self._groups = self.gl.groups.list(all=True)

        return self._groups

    def group_names(self):
        return [g.full_path for g in self.groups]

    def is_group_exists(self, name):
        logging.debug("Try to find group %s in group "
                      "names: %s" % (name, self.group_names()))
        return name in self.group_names()

    def is_project_exists(self, name):
        pass

    def get_group_id_by_name(self, name):
        for g in self.groups:
            if g.full_path == name:
                logging.debug("Found group id by name %s, "
                              "group detailed: %s" % (name, g))
                return g.id

        return None

    def group_projects(self, name):
        group_id = self.get_group_id_by_name(name)
        return self.group_projects_by_id(group_id)

    def group_projects_by_id(self, group_id):
        return self.gl.groups.get(group_id).projects.list(
            all=True, include_subgroups=True)

    def group_project_names(self, name):
        projects = self.group_projects(name)
        return [p.name for p in projects]

    def group_project_names_by_id(self, group_id):
        projects = self.group_projects_by_id(group_id)
        return [p.name for p in projects]

    def create_group(self, namespace):
        logging.info("Create group for %s" % namespace)
        groups = namespace.split("/")
        parent_group_id = None
        for index, g in enumerate(groups):
            current_namespace = "/".join(groups[0:index + 1])
            logging.debug("Current namespace is %s" % current_namespace)
            if not self.is_group_exists(current_namespace):
                logging.debug("Group %s is not exists, "
                              "create it" % current_namespace)
                create_group_info = None
                if not parent_group_id:
                    logging.info("Create root group %s" % g)
                    create_group_info = self.gl.groups.create({
                        "name": g,
                        "path": g
                    })
                else:
                    logging.info("Create sub group %s" % current_namespace)
                    create_group_info = self.gl.groups.create({
                        "name": g,
                        "path": g,
                        "parent_id": parent_group_id
                    })

                parent_group_id = create_group_info.id
                # NOTE(Ray): After create group we need to save into
                # self._group for next loop
                self._groups.append(create_group_info)
            else:
                parent_group_id = self.get_group_id_by_name(current_namespace)
                logging.debug("Group %s is exists, "
                              "group id is %s" % (g, parent_group_id))

        return parent_group_id

    @retry(stop_max_attempt_number=3,
           wait_fixed=60000,
           retry_on_exception=retry_if_timeout)
    def ensure_project_exists(self, namespace, project_name):
        """Create project with namespace"""
        project_url = "%s/%s" % (namespace, project_name)
        logging.info("Ensure project %s "
                     "is exists" % project_url)
        project_group_id = None
        if not self.is_group_exists(namespace):
            logging.info("Can NOT find namespace %s, "
                         "create a new group." % namespace)
            project_group_id = self.create_group(namespace)
        else:
            logging.info("Found namespace %s "
                         "in gitlab" % namespace)
            project_group_id = self.get_group_id_by_name(
                namespace)

        try:
            logging.info("Trying to find project %s" % project_url)
            project = self.gl.projects.get(project_url)
        except requests.exceptions.ReadTimeout as err:
            logging.error("Find project failed due to connection"
                          " timeout by url %s" % project_url)
            raise requests.exceptions.ReadTimeout()
        except gitlab.exceptions.GitlabConnectionError as err:
            logging.error("Find project failed due to connection"
                          " error by url %s" % project_url)
            raise gitlab.exceptions.GitlabConnectionError()
        except Exception as e:
            logging.warn(e)
            logging.info("Project %s CAN NOT be found." % project_url)
            project = None

        if not project:
            logging.info("Creating project %s, namespace_id "
                         "is %s..." % (project_name, project_group_id))
            self.gl.projects.create({
                "name": project_name,
                "namespace_id": project_group_id
            })
