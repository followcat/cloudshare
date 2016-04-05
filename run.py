import os
import glob
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

import webapp.server


app = webapp.server.app
sched = BackgroundScheduler()
atexit.register(lambda: sched.shutdown(wait=True))


def update_lsimodel(app):
    added = False
    lsimodel = app.config['LSI_MODEL']
    for pathfile in glob.glob(os.path.join(app.config['DATA_DB_NAME'], '*.yaml')):
        mdfile = pathfile.replace('.yaml', '.md')
        path, name = mdfile.split('/')
        if os.path.isfile(mdfile) and name not in lsimodel.names:
            data = open(mdfile, 'rb').read()
            lsimodel.add(name, data)
            added = True
    if added:
        lsimodel.save(app.config['LSI_SAVE_PATH'])

if __name__ == '__main__':
    sched.add_job(update_lsimodel, 'interval',seconds=300,
                  args=[app])
    sched.start()
    app.run(debug=True, host='0.0.0.0', port=4888, threaded=True)
