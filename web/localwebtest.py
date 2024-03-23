from flask import Flask
import mimetypes
import os

mimetypes.init()
app = Flask(__name__)

def errorpage(statcode):
	file = open("err.html")
	content = file.read()
	file.close()
	content=content.replace("{STAT}",str(statcode))
	return app.make_response((content, statcode, {'Content-Type':'text/html'}))

@app.route("/",defaults={'path':'index.html'})
@app.route("/<path:path>")
def general(path):
	if os.path.isdir("pages/"+path): path+="/index.html"
	if not os.path.isfile("pages/"+path): return errorpage(404)

	file = open("pages/"+path,"rb")
	content = file.read()
	file.close()

	ctheader = mimetypes.types_map["."+path.rsplit(".",1)[1].strip()]
	return app.make_response((content, 200, {'Content-Type':ctheader}))

if __name__ == '__main__':
	app.run("127.0.0.1",80)