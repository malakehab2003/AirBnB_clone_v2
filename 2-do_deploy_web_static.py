#!/usr/bin/python3

"""
distributes an archive to your web servers
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['100.25.3.157', '3.84.255.36']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

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
    if not exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        filename = archive_path.split('/')[-1]
        folder_name = filename.replace('.tgz', '').split('_')[-1]
        release_path = '/data/web_static/releases/{}'.format(folder_name)

        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(filename, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version
        run('ln -s {} /data/web_static/current'.format(release_path))
        return True
    except Exception as e:
        return False
