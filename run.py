import webapp.server


app = webapp.server.app
if __name__ == '__main__':
    app.debug = True
    if not app.debug:
        import logging
        logger = logging.getLogger()
        handler = logging.handlers.RotatingFileHandler('webapp_flask.log')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    app.run(host='0.0.0.0', port=4888, threaded=True)
