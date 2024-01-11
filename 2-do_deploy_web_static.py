#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers,using the function do_deploy
"""
from fabric.api import *
from fabric.operations import put
from datetime import datetime
import os

env.hosts = ["54.160.117.237", "100.25.31.84"]   # <IP web-01>, <IP web-02>


def do_pack():
    """packages all contents from web_static into .tgz archive
    """
    n = datetime.now().strftime("%Y%m%d%H%M%S")
    local('mkdir -p versions')
    result = local('tar -cvf versions/web_static_{}.tgz web_static'
                   .format(n))
    if result.failed:
        return None
    else:
        return result


def do_deploy(archive_path):
    """Deploys a static archive to my web servers"""

    if not os.path.isfile(archive_path):
        print('archive file does not exist...')
        return False  # Returns False if the file at archive_path doesnt exist
    try:
        archive = archive_path.split('/')[1]
        no_archive_ext = archive.split('.')[0]
    except Exception:
        print('failed to get archive name from split...')
        return False

    uploaded = put(archive_path, '/tmp/')
    if uploaded.failed:
        return False
    Res = run('mkdir -p /data/web_static/releases/{}/'.format(no_archive_ext))
    if Res.failed:
        print('failed to create archive directory for relase...')
        return False
    Res = run('tar -C /data/web_static/releases/{} -xzf /tmp/{}'.format(
               no_archive_ext, archive))
    if Res.failed:
        print('failed to untar archive...')
        return False
    Res = run('rm /tmp/{}'.format(archive))
    if Res.failed:
        print('failed to remove archive...')
        return False
    Res = run('mv /data/web_static/releases/{}/web_static/* \
               /data/web_static/releases/{}'
              .format(no_archive_ext, no_archive_ext))
    if Res.failed:
        print('failed to move extraction to proper directory...')
        return False
    Res = run('rm -rf /data/web_static/releases/{}/web_static'
              .format(no_archive_ext))
    if Res.failed:
        print('failed to remove first copy of extraction after move...')
        return False

    # clean up old release and remove it.

    Res = run('rm -rf /data/web_static/current')
    if Res.failed:
        print('failed to clean up old release...')
        return False
    Res = run('ln -sfn /data/web_static/releases/{} /data/web_static/current'
              .format(no_archive_ext))
    if Res.failed:
        print('failed to create link to new release...')
        return False

    print('\nNew Version Successfuly Deployed!\n')

    return True
