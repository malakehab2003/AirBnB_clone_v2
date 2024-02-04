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
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
