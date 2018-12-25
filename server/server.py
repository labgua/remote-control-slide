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

    master = None

    def open(self):
        print 'Nuova connessione, siamo a pagina %d con url:%s' % (SliderWebsocket.currpage, SliderWebsocket.url)
        self.write_message( 'url##%s' % SliderWebsocket.url )
        self.write_message( 'p%d' % SliderWebsocket.currpage )
        SliderWebsocket.clients.append(self)

    def on_message(self, message):

        print 'Messaggio ricevuto: %s' % message

        if SliderWebsocket.master == None and message == 'master':
            print 'Wellcome Master!!'
            SliderWebsocket.master = self
        
        if self == SliderWebsocket.master:
            print 'Master!! ...'
            if message.startswith("url"):
                url = message.split("##")[1]
                SliderWebsocket.url = url
                SliderWebsocket.currpage = 1

                SliderWebsocket.notifyAll('url##%s' % SliderWebsocket.url)
                SliderWebsocket.notifyAll('p%d' % SliderWebsocket.currpage )

            if message[0] == 'p':
                SliderWebsocket.currpage = int( message.split('p')[1])
                SliderWebsocket.notifyAll('p%d'%SliderWebsocket.currpage)

            if message == 'a':
                SliderWebsocket.dec()

            if message == 'd':
                SliderWebsocket.inc()


    def on_close(self):

        print 'Connessione chiusa'

        if self == SliderWebsocket.master:
            SliderWebsocket.master = None

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
    
    tornado.ioloop.IOLoop.instance().start()