import os
import time

import webapp.settings

import dulwich.porcelain


backup_folders = webapp.settings.BACKUP_DIRS
ISOTIMEFORMAT = '%Y-%m-%d-%X'
source_repo = webapp.settings.DATA_DB.repo
account_repo = webapp.settings.ACCOUNT_DB.repo


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    backup_name = time.strftime(ISOTIMEFORMAT, time.localtime())
    for folder in backup_folders:
        data_backup_path = os.path.join(folder, 'data', backup_name)
        account_backup_path = os.path.join(folder, 'account', backup_name)
        assure_path_exists(data_backup_path)
        assure_path_exists(account_backup_path)
        dulwich.porcelain.clone(source_repo.path, data_backup_path, bare=True)
        dulwich.porcelain.clone(source_repo.path, account_backup_path, bare=True)
