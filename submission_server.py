#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from protocols import FlagServer


def main():
    f = Factory()
    f.protocol = FlagServer
    reactor.listenTCP(8000, f)
    print "Flag server up and running!"
    reactor.run()
    

if __name__ == '__main__':
    main()
