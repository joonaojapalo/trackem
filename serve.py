import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from logger import logger
from routes import app

# read port
port = int(os.environ["PORT"])

# start wsgi server
if app.config["DEBUG"]:
	logger.debug("starting in debug mode. port=%i" % port)
	app.run(debug=True, port=port)
else:
	logger.debug("starting in production mode. port=%i" % port)

	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(port)

	try:
	    IOLoop.instance().start()
	except KeyboardInterrupt:
	    IOLoop.instance().stop()
