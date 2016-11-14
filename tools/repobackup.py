import os
import time

import baseapp.backup
import baseapp.datadbs
import baseapp.projects

import dulwich.porcelain


backup_folders = baseapp.backup.BACKUP_DIRS
ISOTIMEFORMAT = '%Y-%m-%d-%X'
source_repo = baseapp.datadbs.SVC_CV_REPO
account_repo = baseapp.datadbs.SVC_ACCOUNT
medical_repo = baseapp.projects.SVC_PRJ_MED


if __name__ == '__main__':
    backup_name = time.strftime(ISOTIMEFORMAT, time.localtime())
    for folder in backup_folders:
        data_backup_path = os.path.join(folder, 'data', backup_name)
        account_backup_path = os.path.join(folder, 'account', backup_name)
        medical_backup_path = os.path.join(folder, 'medical', backup_name)
        assure_path_exists(data_backup_path)
        assure_path_exists(account_backup_path)
        assure_path_exists(medical_backup_path)
        source_repo.backup(data_backup_path, bare=True)
        account_repo.backup(data_backup_path, bare=True)
        medical_repo.backup(data_backup_path, bare=True)
