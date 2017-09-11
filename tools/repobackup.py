import os
import time
import tarfile

import utils.builtin
import baseapp.backup
import baseapp.datadbs
import baseapp.member
import webapp.settings


backup_folders = baseapp.backup.BACKUP_DIRS
ISOTIMEFORMAT = '%Y-%m-%d-%X'

SVC_MSG = baseapp.datadbs.SVC_MSG
SVC_PWD = baseapp.datadbs.SVC_PWD
SVC_ACCOUNT = baseapp.datadbs.SVC_ACCOUNT

SVC_CV_REPO = baseapp.datadbs.SVC_CV_REPO
SVC_PEO_REPO = baseapp.datadbs.SVC_PEO_REPO
SVC_CV_INDIV = baseapp.datadbs.SVC_CV_INDIV
SVC_PEO_INDIV = baseapp.datadbs.SVC_PEO_INDIV
SVC_MEMBERS =  baseapp.member.SVC_MEMBERS


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
        account_backup_path = os.path.join(folder, 'account', backup_name)
        message_backup_path = os.path.join(folder, 'message', backup_name)
        password_backup_path = os.path.join(folder, 'password', backup_name)
        cvrepo_backup_path = os.path.join(folder, 'cvrepo', backup_name)
        peorepo_backup_path = os.path.join(folder, 'peorepo', backup_name)
        cvindiv_backup_path = os.path.join(folder, 'cvindiv', backup_name)
        peoindiv_backup_path = os.path.join(folder, 'peoindiv', backup_name)
        members_backup_path = os.path.join(folder, 'members', backup_name)
        utils.builtin.assure_path_exists(account_backup_path)
        utils.builtin.assure_path_exists(message_backup_path)
        utils.builtin.assure_path_exists(password_backup_path)
        utils.builtin.assure_path_exists(cvrepo_backup_path)
        utils.builtin.assure_path_exists(peorepo_backup_path)
        utils.builtin.assure_path_exists(cvindiv_backup_path)
        utils.builtin.assure_path_exists(peoindiv_backup_path)
        utils.builtin.assure_path_exists(members_backup_path)
        SVC_MSG.backup(message_backup_path, bare=True)
        SVC_PWD.backup(password_backup_path, bare=True)
        SVC_ACCOUNT.backup(account_backup_path, bare=True)
        SVC_CV_REPO.backup(cvrepo_backup_path, bare=True)
        SVC_PEO_REPO.backup(peorepo_backup_path, bare=True)
        SVC_CV_INDIV.backup(cvindiv_backup_path, bare=True)
        SVC_PEO_INDIV.backup(peoindiv_backup_path, bare=True)
        for member in SVC_MEMBERS.members.values():
            member.backup(members_backup_path)
    backup_upload_output()
