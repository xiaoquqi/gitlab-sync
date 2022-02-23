FROM centos:7

MAINTAINER Ray Sun <xiaoquqi@gmail.com>

ENV LANG en_US.UTF-8

COPY ./src /opt/gitlab-sync
COPY ./requirements.txt /opt/gitlab-sync
COPY ./entrypoint.sh /
COPY ./conf/logrotate/gitlab-sync.conf /etc/logrotate.d/gitlab-sync.conf
WORKDIR /opt/gitlab-sync

RUN yum -y install epel-release && \
    yum clean all && yum makecache && \
    yum -y install cronie logrotate && \
    yum -y install python3 python3-pip git && \
    pip3 install -r requirements.txt && \
    chmod a+x /opt/gitlab-sync/gitlab-sync && \
    chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
