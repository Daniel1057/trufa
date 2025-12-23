import datafrm
import beta
import brp
import tar_brp
from menu import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog
import sys
import subprocess


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	def display_incial(self):
		self.Display.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
										"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
										"p, li { white-space: pre-wrap; }\n"
										"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
										"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
										"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">Bienvenido a Minemas Enduro!!</span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">    </span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">    Rellena las pestañas con las acciones a realizar.</span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">    Tarifa BRP =&gt; Actualiza las tarifas de PRB.</span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">    Tarifa Beta =&gt; Actualiza las tarifas de Beta.</span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">    Despiece BRP =&gt; Descarga despieces de BRP.</span></p>\n"
										"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">    Despiece Beta =&gt; Descarga despieces de Beta.</span></p>\n"
										"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p></body></html>")

	def seleccionar_brp1(self):
		f_ruta = QFileDialog()
		f_ruta = f_ruta.getOpenFileName(self,"Selecciona fichero")
		self.ruta_fichero_1_brp.setText(f_ruta[0])

	def seleccionar_brp2(self):
		f_ruta = QFileDialog()
		f_ruta = f_ruta.getOpenFileName(self,"Selecciona fichero")
		self.ruta_fichero_2_brp.setText(f_ruta[0])

	def seleccionar_beta(self):
		f_ruta = QFileDialog()
		f_ruta = f_ruta.getOpenFileName(self,"Selecciona fichero")
		self.ruta_fichero_beta.setText(f_ruta[0])

	def seleccionar_inventario(self):
		f_ruta = QFileDialog()
		f_ruta = f_ruta.getOpenFileName(self,"Selecciona fichero")
		self.ruta_inventario.setText(f_ruta[0])

	def activar_brp(self):
		if self.Activa_brp.isChecked():
			self.Display.setHtml(
				"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">Seleccionar ficheros excel con las tarifas de BRP.</span></p><font color='green' size='4'><red><br>&nbsp;&nbsp;- Actualizaŕa las referncias y precios en la web.<br>&nbsp;&nbsp;- Generá fichero para Factusol </font>")
			self.ruta_fichero_1_brp.setEnabled(True)
			self.ruta_fichero_2_brp.setEnabled(True)
			self.busca_fichero_1_brp.setEnabled(True)
			self.busca_fichero_2_brp.setEnabled(True)
		else:
			self.ruta_fichero_1_brp.setEnabled(False)
			self.ruta_fichero_2_brp.setEnabled(False)
			self.busca_fichero_1_brp.setEnabled(False)
			self.busca_fichero_2_brp.setEnabled(False)

	def activar_beta(self):

		if self.Activa_beta.isChecked():
			self.Display.setHtml(
				"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">Selecciona fichero excel con la tarifas de Beta.</span></p><font color='green' size='4'><red><br>&nbsp;&nbsp;- Actualizaŕa las referncias y precios en la web.<br>&nbsp;&nbsp;- Generá fichero para Factusol </font>")
			self.ruta_fichero_beta.setEnabled(True)
			self.busca_fichero_beta.setEnabled(True)
		else:
			self.ruta_fichero_beta.setEnabled(False)
			self.busca_fichero_beta.setEnabled(False)
	def activar_spider_beta(self):

		if self.Activa_spider_beta.isChecked():
			self.Display.setHtml(
				"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">Introduce modelo de motos en el cuadro.</span></p><font color='green' size='4'><red><br>&nbsp;&nbsp;- Generá un documento de despiece por cada modelo.<br>&nbsp;&nbsp;- Generá fichero para la web</font>")
			self.Beta_motos.setEnabled(True)
		else:
			self.Beta_motos.setEnabled(False)
	def activar_spider_brp(self):

		if self.Activa_spider_brp.isChecked():
			self.Display.setHtml(
				"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">Introduce tipo, modelo y año.</span></p><font color='green' size='4'><red><br>&nbsp;&nbsp;- Generá un documento de despiece por cada modelo.<br>&nbsp;&nbsp;- Generá fichero para la web</font>")
			self.Anyo_brp.setEnabled(True)
			self.Modelo_brp.setEnabled(True)
			self.Tipo_brp.setEnabled(True)
			self.product.setEnabled(True)
			self.product.addItem('Side by Side')
			self.product.addItem('ATV')
		else:
			self.Anyo_brp.setEnabled(False)
			self.Modelo_brp.setEnabled(False)
			self.Tipo_brp.setEnabled(False)
			self.product.setEnabled(False)
			self.product.clear()


	def aceptar (self):
		print ("Minemas")
		self.Boton_Aceptar.setEnabled(False)
		self.Boton_Aceptar.setHidden(True)
		inventario = self.ruta_inventario.text()
		if self.Activa_spider_beta.isChecked():
			motos = list(str(self.Beta_motos.toPlainText()).split("\n"))
			beta.inicio_beta(motos)
		if self.Activa_spider_brp.isChecked():
			v_anyo = str(self.Anyo_brp.text())
			v_tipo = str(self.Tipo_brp.text())
			v_modelo = str(self.Modelo_brp.text())
			v_product = str(self.product.currentText())
			brp.inicio(v_anyo,v_tipo,v_modelo,v_product)

		if self.Activa_brp.isChecked():
			fichero1 = self.ruta_fichero_1_brp.text()
			fichero2 = self.ruta_fichero_2_brp.text()
			display_brp = tar_brp.inicio_tarifa_brp(fichero1,fichero2,inventario)
			total = display_brp[0]
			duplicados = display_brp[1]
			neto = display_brp[2]
			mensaje = '<br>  Cargadas ' + str(total) + ' referencias.<br>  ' + str(duplicados) + ' referencias duplicadas.<br>  ' + str(neto) + 'Referencias.'
			titulo = 'Ficheros cargados'
			self.Display.setHtml(
				"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
				"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
				"p, li { white-space: pre-wrap; }\n"
				"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
				"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
				"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#c4a000;\">" + titulo + "</span></p>\n"
																																																						"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">    </span></p>\n"
																																																						"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#4e9a06;\">" + mensaje + "</span></p>\n"
																																																																																																				"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p></body></html>")
		self.Boton_Aceptar.setEnabled(True)
		self.Boton_Aceptar.setHidden(False)

	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi (self)

		self.Activa_brp.toggled.connect(self.activar_brp)
		self.Activa_beta.toggled.connect(self.activar_beta)
		self.Activa_spider_brp.toggled.connect(self.activar_spider_brp)
		self.Activa_spider_beta.toggled.connect(self.activar_spider_beta)

		self.busca_fichero_1_brp.clicked.connect(self.seleccionar_brp1)
		self.busca_fichero_2_brp.clicked.connect(self.seleccionar_brp2)
		self.busca_fichero_beta.clicked.connect(self.seleccionar_beta)

		self.busca_inventario.clicked.connect(self.seleccionar_inventario)

		self.Boton_Aceptar.clicked.connect(self.aceptar)



if __name__=="__main__":
	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()
