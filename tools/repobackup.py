import os
import time

import webapp.settings

import dulwich.porcelain


backup_folder = webapp.settings.BACKUP_DIR
ISOTIMEFORMAT = '%Y-%m-%d-%X'
source_repo = webapp.settings.REPO_DB.repo


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    backup_name = time.strftime(ISOTIMEFORMAT, time.localtime())
    backup_path = os.path.join(backup_folder, backup_name)
    assure_path_exists(backup_path)
    dulwich.porcelain.clone(source_repo.path, backup_path, bare=True)
