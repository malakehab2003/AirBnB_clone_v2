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
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive filename without extension>/
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

        print('New version deployed!')
        return True
    except Exception as e:
        return False
