# -*- coding: utf-8 -*-
import aliyun.log as log


class LogHub(object):
    endpoint = None
    access_key_id = None
    access_key = None
    client = None

    def __init__(self, endpoint, access_key_id, access_key):
        self.endpoint = endpoint
        self.access_key_id = access_key_id
        self.access_key = access_key
        self._init_client()

    def _init_client(self):
        self.client = log.LogClient(self.endpoint, self.access_key_id, self.access_key)

    def get_projects(self):
        projects = self.client.list_project()
        return [i["projectName"] for i in projects.body["projects"]]

    def get_logstores(self, project):
        logstores = self.client.list_logstore(project_name=project)
        return logstores.body["logstores"]

    def get_consumer_groups(self, project, logstore):
        consumer_groups = self.client.list_consumer_group(project, logstore)
        return [i["name"] for i in consumer_groups.body]

    def get_check_point(self, project, logstore, consumer_group):
        check_points = self.client.get_check_point(project, logstore, consumer_group)
        return check_points.body


def test():
    endpoint = 'cn-beijing.log.aliyuncs.com'
    # endpoint = "us-west-1.log.aliyuncs.com"
    access_key_id = 'xxx'
    access_key = 'xxx'
    loghub = LogHub(endpoint,access_key_id,access_key)
    for i in loghub.get_projects():
        for j in loghub.get_logstores(i):
            for k in loghub.get_consumer_groups(i, j):
                print i,
                print j,
                print loghub.get_check_point(i, j, k)
                # for l in loghub.get_check_point()
