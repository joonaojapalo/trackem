import os

#from tornado.wsgi import WSGIContainer
#from tornado.httpserver import HTTPServer
#from tornado.ioloop import IOLoop

from routes import app

# read port
port = int(os.environ["PORT"])

if __name__ == "__main__":
	app.run();

	if False:
		# start wsgi server
		http_server = HTTPServer(WSGIContainer(app))
		http_server.listen(port)

		try:
		    IOLoop.instance().start()
		except KeyboardInterrupt:
		    IOLoop.instance().stop()
