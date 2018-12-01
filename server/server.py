import os
import sys
import threading

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

class SliderWebsocket(tornado.websocket.WebSocketHandler):

    url = ""
    currpage = 1
    clients = []

    def open(self):
        print 'Nuova connessione, siamo a pagina %d con url:%s' % (SliderWebsocket.currpage, SliderWebsocket.url)
        self.write_message( 'url##%s' % SliderWebsocket.url )
        self.write_message( 'p%d' % SliderWebsocket.currpage )
        SliderWebsocket.clients.append(self)

    def on_message(self, message):
        # metodo eseguito alla ricezione di un messaggio
        # la stringa 'message' rappresenta il messaggio
        print 'Messaggio ricevuto: %s' % message

    def on_close(self):
        # metodo eseguito alla chiusura della connessione
        print 'Connessione chiusa'
        SliderWebsocket.clients.remove(self)

    def check_origin(self, origin):
        return True



    @staticmethod
    def inc() :
        SliderWebsocket.currpage = SliderWebsocket.currpage + 1
        SliderWebsocket.notifyAll('p%d' % SliderWebsocket.currpage)

    @staticmethod
    def dec() :
        SliderWebsocket.currpage = SliderWebsocket.currpage - 1
        SliderWebsocket.notifyAll('p%d' % SliderWebsocket.currpage)

    @staticmethod
    def notifyAll(msg) :
        print 'NOTIFICO %s' % msg
        for c in SliderWebsocket.clients:
            c.write_message(msg)


path = os.getcwd();

application = tornado.web.Application([
    (r'/websocketserver', SliderWebsocket),
    ('/(.*\..*)', tornado.web.StaticFileHandler, {'path': path + "/../slider"})
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    
    # RUNNING TORNADO IN BACKGROUND
    # with method -> tornado.ioloop.IOLoop.instance().start()
    tornadoInstance = tornado.ioloop.IOLoop.instance()
    
    t = threading.Thread(target=tornadoInstance.start)
    t.start()

    SliderWebsocket.url = "slide.pdf"
    SliderWebsocket.currpage = 1

    while 1:
        line = sys.stdin.readline()
        line = line.replace('\n','')

        if line == '':
            continue

        print 'ricevuto |%s|' % line

        if line == 'exit':
            break

        if line.startswith("url"):
            url = line.split("##")[1]
            SliderWebsocket.url = url
            SliderWebsocket.currpage = 1

        if line[0] == 'p':
            page = int( line.split('p')[1])
            SliderWebsocket.currpage = page
            SliderWebsocket.notifyAll('p%d'%page)

        if line == 'a':
            SliderWebsocket.dec()

        if line == 'd':
            SliderWebsocket.inc()

    t.do_run = False
    t.join()

    print("after join")