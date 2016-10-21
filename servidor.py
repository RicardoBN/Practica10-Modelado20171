from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys, time
from PyQt4 import QtCore, QtGui, uic
from random import randint

estado = 0
estado_ter = 0
serpientes = dict()
serpiente = []
dir = 3
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
class Serpiente:
   def __init__(self, tamaño,id):
    self.tamaño = tamaño
    self.cuerpo = []
    self.id = id
    self.genera_cuerpo()    
    self.color = []
    self.colorea()
    self.direccion = 3

   def dame_color(self):
    return "'r': "+str(self.color[0])+", 'g': "+str(self.color[1])+", 'b': "+str(self.color[2])
   def datos(self):
    return "{id: "+str(self.id)+",\n 'camino': "+ str(self.cuerpo)+",\n 'color': "+ self.dame_color()+"\n}"
    
   def genera_cuerpo(self):
    for x in range(0,self.tamaño):
      self.cuerpo.append([x,int(self.id)])  

   def colorea(self):
    self.color.append(randint(1,255))
    self.color.append(randint(1,255))
    self.color.append(randint(1,255))
   def cambia_dir(self,dir):
    self.direccion = dir 

class Servidor(QtGui.QMainWindow):
    def __init__(self): 
        super(Servidor, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.clicked.connect(self.focus)
        self.spinBox.valueChanged.connect(self.cambia_columnas)
        self.spinBox_2.valueChanged.connect(self.cambia_filas)
        self.doubleSpinBox.valueChanged.connect(self.cambia_ms)
        self.pushButton_2.clicked.connect(self.inicia)
        self.pushButton_3.clicked.connect(self.termina)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.corre_juego)
        self.k = self.doubleSpinBox.value()
        self.timer.setInterval(self.k)
        self.pushButton.clicked.connect(self.inicia_servidor)             
        self.setFocus()
        self.show()    
          
    # Cambio de Movimiento    
    def keyPressEvent(self, event):
      global dir
      key = event.key()      
      if key == QtCore.Qt.Key_Left and dir != 4:
        dir = 2              
      if key == QtCore.Qt.Key_Right and dir != 2:
        dir = 4                
      if key == QtCore.Qt.Key_Up and dir != 3:
        dir = 1                
      if key == QtCore.Qt.Key_Down and dir != 1:
        dir = 3         
    # Inicio del juego     
    def inicia(self):
      global estado      
      print(estado)          
      self.pushButton_3.setText("Terminar")
      self.setFocus()      
      if estado == 0:
        estado = 1        
        self.yo_juego()        
        self.colorea_serpientes()
        self.pushButton_2.setText("Pausar")
        self.corre_juego()
        self.timer.start()  
      elif estado == 1:
        estado = 2
        self.pushButton_2.setText("Renaudar")
        self.timer.stop()  
      elif estado == 2:
        estado = 1
        self.pushButton_2.setText("Pausar")
        self.corre_juego()
        self.timer.start()  
      elif estado == 3:
        estado = 0
        self.inicia()    
    #Terminar el juego
    def corre_juego(self):           
      self.cambia_ms()
      self.mueve_serpiente(serpientes[0],dir)
      #self.server.handle_request()    
    def termina(self):
      global estado
      global dir             
      estado = 3
      dir = 3
      print("El juego ha terminado")
      self.timer.stop()
      self.pushButton_2.setText("Reiniciar")
      self.tableWidget.setColumnCount(0)
      self.tableWidget.setRowCount(0)
      self.tableWidget.setColumnCount(0)
      self.spinBox_2.setProperty("value", 20)
      self.spinBox.setProperty("value", 20)
      self.doubleSpinBox.setProperty("value", 30.00)
      self.tableWidget.setColumnCount(self.spinBox.value())
      self.tableWidget.setRowCount(self.spinBox_2.value())
      serpientes.clear()
    #Cambia el delay del programa y en este se actualizan las serpientes    
    def cambia_ms(self):
      global dir         
      tiempo = self.doubleSpinBox.value()      
      self.timer.setInterval(tiempo)
      

    #Quita la cola y actualiza la cabeza con respecto a la dirección    
    def mueve_serpiente(self,serp,direc):
           
      self.tableWidget.item(serp.cuerpo[0][0],serp.cuerpo[0][1]).setBackground(QtGui.QColor(255,255,255))
      limit_col = int(self.spinBox.value())-1
      limit_row = int(self.spinBox_2.value())-1
      cabeza = serp.cuerpo[-1]
      serp.cuerpo.pop(0)
      if direc == 1:
        if cabeza != [0, serp.cuerpo[-1][1]]: 
          serp.cuerpo.append([serp.cuerpo[-1][0]-1,serp.cuerpo[-1][1]]) #Movimiento hacia arriba
        else:
          serp.cuerpo.append([limit_row,serp.cuerpo[-1][1]])
      if direc == 2:
        if cabeza != [serp.cuerpo[-1][0],0]:
          serp.cuerpo.append([serp.cuerpo[-1][0],serp.cuerpo[-1][1]-1]) #Movimiento hacia la izquierda                                      
        else:
          serp.cuerpo.append([serp.cuerpo[-1][0], limit_row])
      if direc == 3:
        if cabeza != [limit_row, serp.cuerpo[-1][1]]:
          serp.cuerpo.append([serp.cuerpo[-1][0]+1,serp.cuerpo[-1][1]]) #Movimiento hacia abajo
        else:
          serp.cuerpo.append([0,serp.cuerpo[-1][1]])
      if direc == 4: 
        if cabeza != [serp.cuerpo[-1][0],limit_col]:
         serp.cuerpo.append([serp.cuerpo[-1][0], serp.cuerpo[-1][1]+1]) #Movimiento havia la derecha
        else:    
          serp.cuerpo.append([serp.cuerpo[-1][0], 0])
      for x in range(0,len(serp.cuerpo)-1):        
        self.colorea_serpientes()
      for cuerpo in serp.cuerpo:
        if serp.cuerpo.count(cuerpo)>1:
          self.termina()
    #Cambio de columnas dinámico        
    def cambia_columnas(self):
      Columnas = int(self.tableWidget.columnCount())
      total = int(self.spinBox.value())
      if Columnas >= total:
        while Columnas >= total:
          self.tableWidget.removeColumn(Columnas)
          Columnas -= 1
      elif Columnas < total:
        while Columnas < total:
          self.tableWidget.insertColumn(Columnas)
          Columnas += 1
    #Cambio de filas dinámico      
    def cambia_filas(self):
      filas = int(self.tableWidget.rowCount())
      total = int(self.spinBox_2.value())
      if filas >= total:
        while filas >= total:
          self.tableWidget.removeRow(filas)
          filas -= 1
      elif filas < total:
        while filas < total:
          self.tableWidget.insertRow(filas)
          filas += 1      
               
    def colorea_serpientes(self):
      for x in serpientes.values():
        for cuerpo in x.cuerpo:
          self.tableWidget.setItem(cuerpo[0],cuerpo[1], QtGui.QTableWidgetItem())
          self.tableWidget.item(cuerpo[0],cuerpo[1]).setBackground(QtGui.QColor(x.color[0],x.color[1],x.color[2]))
    def focus(self):
      self.setFocus()            
    def ping(self):
      return "¡Pong!"
    def yo_juego(self):
      serpiente = Serpiente(11,len(serpientes))      
      serpientes[len(serpientes)] = serpiente
      datos = "{'id': "+str(serpiente.id)+", 'color': "+serpiente.dame_color()+"}"
      return datos
    def cambia_direccion(self,id,dir):
       serpientes[id].cambia_dir(dir)
       return (str(serpientes[id])+"ha cambiado de direccion a"+str(dir))
    def estado_del_juego(self):
      datos = ("{\n"+
                 "'espera': "+str(self.doubleSpinBox.value())+"\n"+                 
                 "'tamaño X': "+str(self.spinBox_2.value())+"\n"+
                 "'tamaño Y': "+str(self.spinBox.value())+"\n"+
                 "'serpientes: ")
      for x in serpientes.values():
        datos+= str(x.datos())

      return datos
    def inicia_servidor(self):      
      servidor = self.lineEdit.text()
      puerto = 1 #self.spinBox_4.value()
      timeout = self.spinBox_5.value()
      print("Servidor iniciado Servidor: "+str(servidor)+" puerto: "+str(puerto)+" timeout: "+ str(timeout))     
    # Create server
      server = SimpleXMLRPCServer(("localhost",puerto))
      server.register_multicall_functions()      
      server.register_function(self.ping,'ping')
      server.register_function(self.yo_juego,'yo_juego')
      server.register_function(self.cambia_direccion,'cambia_direccion')
      server.register_function(self.estado_del_juego,'estado_del_juego')
      server.register_introspection_functions()
      for x in range(0,7):
        server.handle_request()
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    serv = Servidor()
    sys.exit(app.exec_())        
        
