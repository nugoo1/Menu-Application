from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
            	output += "<html><body>"
               	items = session.query(Restaurant).all()
               	
               	n = 1
                for item in items:
                	output += "<h2>"
                	output += item.name
                	output += "</h2>"
               		output += "<a href='"
               		output += "%s" % n
               		output += "/edit'>Edit</a>"
               		output += "<br>"
               		output += "<a href=#> Delete</a>"
               		output += "<br><br>"
               		n = n+1

               	output += "<a href='/new'> Create New Restaurant</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'><input name="newRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                p = self.path.split("/")[1]
                restaurantName = session.query(Restaurant).filter_by(id = p).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant</h1>"
                output += "<h2>"
                output += restaurantName.name
                output += "</h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new'><input name="editRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
               	fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurant')
            	newRestaurant = Restaurant(name = messagecontent[0])
            	session.add(newRestaurant)
            	session.commit()

           	if ctype == 'multipart/form-data':
           		fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('editRestaurant')
                p = self.path.split("/")[1]
                restaurantName = session.query(Restaurant).filter_by(name = p).one()
                restaurantName.name = messagecontent[0]
                session.add(restaurant)
            	session.commit()

        except:
            pass


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()