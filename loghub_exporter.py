# -*- coding: utf-8 -*-
from loghub import LogHub
import prometheus_client
import flask
import time
import click

app = flask.Flask(__name__)

index_html = """
<html>
    <head><title>Prometheus Exporter</title></head>
    <body>
        <h1>LogHub Prometheus Exporter</h1>
        <p><a href='/metrics'>Metrics</a></p>
    </body>
</html>
"""

REGISTRY = prometheus_client.CollectorRegistry(auto_describe=False)
g_check_point_shard = prometheus_client.Gauge('loghub_check_point_shard', 'loghub check_point'
                                              , ['endpoint', 'project', 'logstore', 'consumer_group', 'shard']
                                              , registry=REGISTRY)
g_check_point = prometheus_client.Gauge('loghub_check_point', 'loghub check_point'
                                        , ['endpoint', 'project', 'logstore', 'consumer_group']
                                        , registry=REGISTRY)

app_endpoints = []
app_access_key_id = ""
app_access_key = ""


@app.route('/')
def index():
    return index_html


@app.route("/metrics")
def metrics():
    try:
        for endpoint in app_endpoints:
            loghub = LogHub(endpoint, app_access_key_id, app_access_key)
            for project in loghub.get_projects():
                for logstore in loghub.get_logstores(project):
                    for consumer_group in loghub.get_consumer_groups(project,logstore):
                        exec_time = time.time()
                        time_diff_all = 0
                        for shard in loghub.get_check_point(project, logstore, consumer_group):
                            time_diff = int(exec_time - shard["updateTime"]/1000000)
                            time_diff_all = time_diff_all + time_diff
                            g_check_point_shard.labels(endpoint=endpoint, project=project
                                                       , logstore=logstore, consumer_group=consumer_group
                                                       , shard=shard["shard"]).set(float(time_diff))
                        g_check_point.labels(endpoint=endpoint, project=project
                                             , logstore=logstore, consumer_group=consumer_group).set(float(time_diff_all))
    except Exception, e:
        print e
    return flask.Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


@click.command()
@click.option("-e", "--endpoints", type=str, help=u"endpoints `,`分割.默认:cn-beijing.log.aliyuncs.com,us-west-1.log.aliyuncs.com",
              default=u"cn-beijing.log.aliyuncs.com,us-west-1.log.aliyuncs.com")
@click.option("-k", "--access_key_id", type=str, help=u"阿里云access_key_id", default=u"")
@click.option("-a", "--access_key", type=str, help=u"阿里云access_key", default=u"")
@click.option("-p", "--port", type=str, help=u"端口,默认:8001", default=u"8001")
def run(endpoints, access_key_id, access_key, port):
    global app_endpoints, app_access_key_id, app_access_key
    app_endpoints = endpoints.split(",")
    app_access_key_id = access_key_id
    app_access_key = access_key
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    run()
