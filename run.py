import atexit

from apscheduler.schedulers.background import BackgroundScheduler

import webapp.server


app = webapp.server.app
sched = BackgroundScheduler()
atexit.register(lambda: sched.shutdown(wait=True))


if __name__ == '__main__':
    sched.add_job(app.config['SVC_MIN'].update_sims, 'cron', hour='23')
    sched.add_job(app.config['SVC_MIN'].update_model, 'cron', hour='2')
    sched.start()
    app.run(debug=False, host='0.0.0.0', port=4888, threaded=True)
