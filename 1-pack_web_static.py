#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder
of your AirBnB Clone repo,
using the function do_pack
"""

import datetime
from fabric.api import local


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"web_static_{date}.tgz"
    local("mkdir -p versions")
    return local(f"tar -czvf {name} versions")
