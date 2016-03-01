import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from logger import logger
from routes import app

# read port
port = int(os.environ["PORT"])
logger.debug("port=%i" % port)

# start wsgi server
app.run(debug=True, port=port)

if False:
	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(port)

	try:
	    IOLoop.instance().start()
	except KeyboardInterrupt:
	    IOLoop.instance().stop()
