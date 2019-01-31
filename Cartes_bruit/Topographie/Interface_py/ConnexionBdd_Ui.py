# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Martin\.eclipse\workspace\Utiliser_Base_Bruit\source\Interface\FichierUi\ConnexionBdd.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogConnexionBdd(object):
    def setupUi(self, DialogConnexionBdd):
        DialogConnexionBdd.setObjectName("DialogConnexionBdd")
        DialogConnexionBdd.resize(325, 191)
        self.gridLayout = QtWidgets.QGridLayout(DialogConnexionBdd)
        self.gridLayout.setObjectName("gridLayout")
        self.nomBdd = QtWidgets.QLineEdit(DialogConnexionBdd)
        self.nomBdd.setObjectName("nomBdd")
        self.gridLayout.addWidget(self.nomBdd, 2, 1, 1, 1)
        self.labelBaseDeDonnee = QtWidgets.QLabel(DialogConnexionBdd)
        self.labelBaseDeDonnee.setObjectName("labelBaseDeDonnee")
        self.gridLayout.addWidget(self.labelBaseDeDonnee, 2, 0, 1, 1)
        self.labelHote = QtWidgets.QLabel(DialogConnexionBdd)
        self.labelHote.setObjectName("labelHote")
        self.gridLayout.addWidget(self.labelHote, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogConnexionBdd)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 1, 1, 1)
        self.labelMotDePasse = QtWidgets.QLabel(DialogConnexionBdd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMotDePasse.sizePolicy().hasHeightForWidth())
        self.labelMotDePasse.setSizePolicy(sizePolicy)
        self.labelMotDePasse.setObjectName("labelMotDePasse")
        self.gridLayout.addWidget(self.labelMotDePasse, 5, 0, 1, 1)
        self.motDePasse = QtWidgets.QLineEdit(DialogConnexionBdd)
        self.motDePasse.setObjectName("motDePasse")
        self.gridLayout.addWidget(self.motDePasse, 5, 1, 1, 1)
        self.labelUtilisateur = QtWidgets.QLabel(DialogConnexionBdd)
        self.labelUtilisateur.setObjectName("labelUtilisateur")
        self.gridLayout.addWidget(self.labelUtilisateur, 3, 0, 1, 1)
        self.nomUtilisateur = QtWidgets.QLineEdit(DialogConnexionBdd)
        self.nomUtilisateur.setObjectName("nomUtilisateur")
        self.gridLayout.addWidget(self.nomUtilisateur, 3, 1, 1, 1)
        self.nomHote = QtWidgets.QLineEdit(DialogConnexionBdd)
        self.nomHote.setObjectName("nomHote")
        self.gridLayout.addWidget(self.nomHote, 1, 1, 1, 1)
        self.labelTitreBase1 = QtWidgets.QLabel(DialogConnexionBdd)
        self.labelTitreBase1.setObjectName("labelTitreBase1")
        self.gridLayout.addWidget(self.labelTitreBase1, 0, 0, 1, 2)

        self.retranslateUi(DialogConnexionBdd)
        self.buttonBox.accepted.connect(DialogConnexionBdd.accept)
        self.buttonBox.rejected.connect(DialogConnexionBdd.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogConnexionBdd)

    def retranslateUi(self, DialogConnexionBdd):
        _translate = QtCore.QCoreApplication.translate
        DialogConnexionBdd.setWindowTitle(_translate("DialogConnexionBdd", "Connexion a 1 ou 2 base de donnees"))
        self.labelBaseDeDonnee.setText(_translate("DialogConnexionBdd", "Base de donnees"))
        self.labelHote.setText(_translate("DialogConnexionBdd", "Hote"))
        self.labelMotDePasse.setText(_translate("DialogConnexionBdd", "Mot de passe"))
        self.labelUtilisateur.setText(_translate("DialogConnexionBdd", "Utilisateur"))
        self.labelTitreBase1.setText(_translate("DialogConnexionBdd", "Base de donnees 1"))

