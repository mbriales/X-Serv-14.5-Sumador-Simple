#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Author: Miguel Briales Romanillos
Funcionamiento del programa:
1. Introducir en barra de direcciones: localhost:1234/num
2. Introducir de nuevo en barra de direcciones localhost:1234/otro_num
3. Mientras se haga sucesivamente los números se iran sumando a
la suma anterior

Explanation:
class appApp: Parses request and Estimates sum
class webApp: webApp + Rules
Runs the program
"""
import socket


class appApp:
    def parse(self, request):
        summand = request.split()[1][1:]
        return summand

    def estimator(self, summand, estimate):
        estimate = int(estimate) + int(summand)
        return estimate


class webApp:
    def __init__(self):
        # Some variables
        round = 'first'
        call = 'first'
        # CREATE TCP OBJECT SOCKET AND BIND IT TO PORT
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind(("localhost", 1222))
        mySocket.listen(5)

        # ACCEPT CONNECTIONS, READ INCOMING DATA AND ANSWER BACK
        while True:
            try:
                # GETS INBOUND CALL
                print 'Waiting for connections'
                (recvSocket, address) = mySocket.accept()
                request = recvSocket.recv(2048)
                print 'Request received:'
                print request
                # As always 2 GETS are received, 'if' only takes
                # the first GET call
                if call == 'first':
                    call = 'nexts'
                    app = appApp()
                    summand = app.parse(request)
                # Distinguish between first iteraction and next ones in
                # order to be consistent with the estimate
                    if round == 'first':
                        estimate = int(summand)
                        round = 'other'
                    else:
                        estimate = app.estimator(summand, estimate)
                else:
                    call = 'first'
                # ANSWERS OUTBOUND CALL
                print 'Answering back...'
                recvSocket.send('HTTP/1.1 200 OK\r\n\r\n' +
                                '<html><body>' +
                                '<p>Tu suma es: %s' % str(estimate) +
                                '</p>' + '</body></html>\r\n')
                recvSocket.close()
            # EXCEPTIONS
            except KeyboardInterrupt:
                print 'Closing binded socket'
                mysocket.close()
            except ValueError:
                print 'Value Error'
                print 'Answering back...'
                recvSocket.send('HTTP/1.1 200 OK\r\n\r\n' +
                                '<html><body>' +
                                '<p>Tu suma previa era: ' +
                                '%s' % str(estimate) +
                                '<br /> Introduce un valor númerico!' +
                                '</p>' + '</body></html>\r\n')
                recvSocket.close()


# RUNS THE PROGRAM
webApp()
