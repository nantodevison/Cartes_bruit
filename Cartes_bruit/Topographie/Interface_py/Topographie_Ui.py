# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Martin\.eclipse\workspace\Utiliser_Base_Bruit\source\Interface\FichierUi\Topographie.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogTopographie(object):
    def setupUi(self, DialogTopographie):
        DialogTopographie.setObjectName("DialogTopographie")
        DialogTopographie.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogTopographie)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BoutonCreerDalage = QtWidgets.QPushButton(DialogTopographie)
        self.BoutonCreerDalage.setObjectName("BoutonCreerDalage")
        self.horizontalLayout.addWidget(self.BoutonCreerDalage)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioBouton_dalleRge = QtWidgets.QRadioButton(DialogTopographie)
        self.radioBouton_dalleRge.setObjectName("radioBouton_dalleRge")
        self.verticalLayout_2.addWidget(self.radioBouton_dalleRge)
        self.radioBouton_dalleBd = QtWidgets.QRadioButton(DialogTopographie)
        self.radioBouton_dalleBd.setObjectName("radioBouton_dalleBd")
        self.verticalLayout_2.addWidget(self.radioBouton_dalleBd)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.BoutonCreerXYZ = QtWidgets.QPushButton(DialogTopographie)
        self.BoutonCreerXYZ.setObjectName("BoutonCreerXYZ")
        self.verticalLayout.addWidget(self.BoutonCreerXYZ)

        self.retranslateUi(DialogTopographie)
        QtCore.QMetaObject.connectSlotsByName(DialogTopographie)

    def retranslateUi(self, DialogTopographie):
        _translate = QtCore.QCoreApplication.translate
        DialogTopographie.setWindowTitle(_translate("DialogTopographie", "Dialog"))
        self.BoutonCreerDalage.setText(_translate("DialogTopographie", "Créer Dallage dans Bdd"))
        self.radioBouton_dalleRge.setText(_translate("DialogTopographie", "Dallage dans RgeAlti"))
        self.radioBouton_dalleBd.setText(_translate("DialogTopographie", "dallage dans BdAlti"))
        self.BoutonCreerXYZ.setText(_translate("DialogTopographie", "Créer les points cotés dans la Bdd"))

