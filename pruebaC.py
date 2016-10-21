import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:1')
print(s.ping())  
print(s.yo_juego())
print(s.cambia_direccion(0,2))
print(s.yo_juego())
print(s.estado_del_juego())  
print(s.system.listMethods())
