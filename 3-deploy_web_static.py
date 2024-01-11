#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)
 that creates and distributes an archive to your web servers,
 using the function deploy:
"""

from datetime import datetime
import os.path
from fabric.api import put, run, env, local

env.hosts = ['54.160.117.237', '100.25.31.84']  # <IP web-01>, <IP web-02>


def do_pack():
    """
    making an .tgz archive from the content to the web_static folder
    """
    date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file_name)).failed is True:
        return None
    return file_name


def do_deploy(archive_path):
    """Distributes an archive to my web servers.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False  # Returns False if the file at archive_path doesnt exist
    file_name = archive_path.split("/")[-1]
    name = file_name.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file_name, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file_name)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """
    Create and distribute an archive to a web server
    """
    file = do_pack()
    if file_name is None:
        return False
    return do_deploy(file_name)
