#!/usr/bin/python3

"""
distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['100.25.3.157', '3.84.255.36']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/fabric'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Create the archive name based on current timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    # Compress the web_static folder into the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive has been correctly generated
    if result.succeeded:
        return f'versions/{archive_name}'
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
