import webapp.server


app = webapp.server.app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4888, threaded=True)
