from Dtoy import app,socketio


if __name__ == '__main__':
	# app.run(debug=True,host='0.0.0.0',port=15000)
    socketio.run(app, debug=True,host='0.0.0.0',port=15000)

