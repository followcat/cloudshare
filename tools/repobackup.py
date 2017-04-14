import os
import time
import tarfile

import utils.builtin
import baseapp.backup
import baseapp.datadbs
import baseapp.projects
import webapp.settings


backup_folders = baseapp.backup.BACKUP_DIRS
ISOTIMEFORMAT = '%Y-%m-%d-%X'
source_repo = baseapp.datadbs.SVC_CV_REPO
account_repo = baseapp.datadbs.SVC_ACCOUNT
company_repo = baseapp.datadbs.SVC_CO_REPO
medical_repo = baseapp.projects.SVC_PRJ_MED
AI_repo = baseapp.projects.SVC_PRJ_AI
BT_repo = baseapp.projects.SVC_PRJ_BT
IA_repo = baseapp.projects.SVC_PRJ_IA
NE_repo = baseapp.projects.SVC_PRJ_NE

def backup_upload_output():
    for folder in backup_folders:
        output_backup_path = os.path.join(folder, 'data', 'upload_output.tar.gz')
        tar = tarfile.open(output_backup_path, 'w:gz')
        for root, dir, files in os.walk(webapp.settings.UPLOAD_TEMP):
            for file in files:
                fullpath=os.path.join(root, file)
                tar.add(fullpath, arcname=file)
        tar.close()

if __name__ == '__main__':
    backup_name = time.strftime(ISOTIMEFORMAT, time.localtime())
    for folder in backup_folders:
        data_backup_path = os.path.join(folder, 'data', backup_name)
        account_backup_path = os.path.join(folder, 'account', backup_name)
        medical_backup_path = os.path.join(folder, 'medical', backup_name)
        company_backup_path = os.path.join(folder, 'company', backup_name)
        AI_backup_path = os.path.join(folder, 'AI', backup_name)
        BT_backup_path = os.path.join(folder, 'BT', backup_name)
        IA_backup_path = os.path.join(folder, 'IA', backup_name)
        NE_backup_path = os.path.join(folder, 'NE', backup_name)
        utils.builtin.assure_path_exists(data_backup_path)
        utils.builtin.assure_path_exists(account_backup_path)
        utils.builtin.assure_path_exists(company_backup_path)
        utils.builtin.assure_path_exists(medical_backup_path)
        utils.builtin.assure_path_exists(AI_backup_path)
        utils.builtin.assure_path_exists(BT_backup_path)
        utils.builtin.assure_path_exists(IA_backup_path)
        utils.builtin.assure_path_exists(NE_backup_path)
        source_repo.backup(data_backup_path, bare=True)
        account_repo.backup(account_backup_path, bare=True)
        company_repo.backup(company_backup_path, bare=True)
        medical_repo.backup(medical_backup_path, bare=True)
        AI_repo.backup(AI_backup_path, bare=True)
        BT_repo.backup(BT_backup_path, bare=True)
        IA_repo.backup(IA_backup_path, bare=True)
        NE_repo.backup(NE_backup_path, bare=True)
    backup_upload_output()
