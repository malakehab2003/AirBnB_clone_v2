#!/usr/bin/python3

"""
distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['100.25.3.157', '3.84.255.36']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None

def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if os.path.exists(archive_path) is False:
        return (False)
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False
    name = archive_path.split("/")[-1].split(".")[0]
    result = run(
        f"mkdir -p /data/web_static/releases/{name}")
    if result.failed:
        return False
    result = run(
        f"tar -xvf /tmp/{name}.tgz -C /data/web_static/releases/{name}")
    if result.failed:
        return False
    result = run(
        f"mv /data/web_static/releases/{name}/web_static/* \
          /data/web_static/releases/{name}")
    if result.failed:
        return False
    result = run(f"rm /tmp/{name}.tgz")
    if result.failed:
        return False
    result = run(
        f"rm /data/web_static/current")
    if result.failed:
        return False
    result = run(
        f"ln -sf /data/web_static/releases/{name} /data/web_static/current")
    if result.failed:
        return False
    return True
