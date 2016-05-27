import os
import glob
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

import webapp.server


app = webapp.server.app
sched = BackgroundScheduler()
atexit.register(lambda: sched.shutdown(wait=True))


if __name__ == '__main__':
    sched.add_job(app.config['SVC_MIN'].update, 'interval', seconds=300)
    sched.start()
    app.run(debug=True, host='0.0.0.0', port=4888, threaded=True)
