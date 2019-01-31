'''
#*coding utf-8*#
Created on 19 avr. 2017

@author: Martin
'''

import psycopg2
from osgeo import ogr
import sys, os
from Martin_Perso.Connexion_Transfert import ConnexionBdd, Ogr2Ogr
import subprocess
from Topographie.Interface_py.ConnexionBdd_Ui import Ui_DialogConnexionBdd
from Topographie.Interface_py.Topographie_Ui import Ui_DialogTopographie
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QMessageBox

class ConnexionBdd_Ui(QDialog,Ui_DialogConnexionBdd):
    '''
    Classe pour connexion à une base de donnees postgres
    '''

    def __init__(self, serveur='localhost', bdd='Bdd_BAU', user='postgres', mdp='postgres',schema='public', table='tmp',parent=None):
        '''
        Constructeur
        '''
        parametre=ConnexionBdd()
        self.setupUi(self)#recuperation de la methode setupUi de la classe mere
        #affectation des variables dans les textes de l'Ui
        self.nomHote.setText(parametre.serveur)
        self.nomBdd.setText(parametre.bdd) 
        self.nomUtilisateur.setText(parametre.user)
        self.motDePasse.setText(parametre.mdp)
        #attributs supplementaires
        self.schema=parametre.schema
        self.table=parametre.table
        self.buttonBox.accepted.connect(ConnexionBdd.creerConnexion())
        

class Topographie(QDialog,Ui_DialogTopographie):
    '''
    Classe pour afficher le dialog sur la topo
    '''
    
    def __init__(self,parent=None):
        super(Topographie,self).__init__(parent)
        self.setupUi(self)
        self.BoutonCreerDalage.clicked.connect(self.CreerDalage)
        self.BoutonCreerXYZ.clicked.connect(self.CreerXyz)
        
    def CreerDalage(self):
        """Creer le dalage de fichiers .ASC à partir d'un dossier"""
        #ouvrir une connexion avec la Bdd postgis
        connecterBdd=ConnexionBdd_Ui()
        connecterBdd.exec_()
        print (connecterBdd.connstringPsy)
        if connecterBdd:
            
            #creer un fichier shp de dallage
            dossierEntre=os.path.abspath(QFileDialog.getExistingDirectory(self,"Open a folder",'E:\\Boulot\\BaseDeDonnees\\Topographie\\RGEAlti\\1m',QFileDialog.ShowDirsOnly))
            fichierSortie=dossierEntre+"\\temp.shp"
            fichierEntre=dossierEntre+"\\*.asc"
            redirection_gdaldata="cd C:\Program Files\GDAL\gdal-data"
            commandeGdal='gdaltindex -tileindex nom_dalle -t_srs EPSG:2154 -write_absolute_path %s %s'%(fichierSortie, fichierEntre)
            cmd=redirection_gdaldata+" && "+commandeGdal
            subprocess.call(cmd,shell=True)
            
            #determiner quel table de dallage est a impacter
            if self.radioBouton_dalleRge.isChecked():
                tableDallage='dalles_rgealti'
            else:
                tableDallage='dalles_bdalti'
            
            #passer le dallage dans postgres
            importer=Ogr2Ogr()
            importer.shp2pg(connecterBdd.connstringOgr, fichierSortie, 'topographie', tableDallage, '2154', 'POLYGON', 2,'-update -append')
            
            #mettre à jour le nom des dalles dans postgres
            curseurPsy=connecterBdd.connexionPsy.cursor()
            curseurPsy.execute("UPDATE topographie.%s SET nom_dalle=reverse(split_part(reverse(nom_dalle),\'\\\',1))"%(tableDallage))
            curseurPsy.close()
            connecterBdd.connexionPsy.commit()
            
            #supprimer les fichiers de dallage
            os.remove(fichierSortie)
            os.remove(fichierSortie[:-4]+'.dbf')
            os.remove(fichierSortie[:-4]+'.prj')
            os.remove(fichierSortie[:-4]+'.shx')
        
        BoiteMessage('fin créartion des dalles','tout fait')    
            
    def CreerXyz(self,codeDept):
        """Creer fichier xyz a partir de dalle et de lineaire dans postgres"""
        ######################## A FAIRE : ajouter un widget de choix du departement############################################
        codeDept='086'
        connecterBdd=ConnexionBdd_Ui()
        connecterBdd.exec_()
        if connecterBdd:
            
            #nom du dossier contenant les fichiers .asc
            dossierEntreRge=os.path.abspath(QFileDialog.getExistingDirectory(self,"choisir le dossier des fichiers RGEALTI",'E:\\Boulot\\BaseDeDonnees\\Topographie\\RGEAlti\\1m',QFileDialog.ShowDirsOnly))
            dossierEntreBdalti=os.path.abspath(QFileDialog.getExistingDirectory(self,"choisir le dossier des fichiers BDALTI",'E:\\Boulot\\BaseDeDonnees\\Topographie\\RGEAlti\\1m',QFileDialog.ShowDirsOnly))
            
            #extraction des dalles
            curseurPsy=connecterBdd.connexionPsy.cursor()
            curseurPsy2=connecterBdd.connexionPsy.cursor()
            ######################### A FAIRE : il faudra ajouter un refresh des vue matérialisee de zonage############################################
            curseurPsy.execute("SELECT DISTINCT rg.nom_dalle FROM topographie.dalles_rgealti AS rg, zonage.zone_precision as d WHERE ST_Intersects(rg.geom,d.geom) AND d.code_dept=\'%s\' UNION SELECT DISTINCT bd.nom_dalle FROM topographie.dalles_bdalti AS bd, zonage.zone_etude as d WHERE ST_Intersects(d.geom,bd.geom) AND d.code_dept=\'%s\' ORDER BY nom_dalle DESC "%(codeDept,codeDept)) #on trie la query pour traiter les RGE (et donc les nodata) en premier
            importer=Ogr2Ogr()
            #print(curseurPsy.fetchone())
            
            #boucle sur la liste de dalle pour creation des points
            for fichierAsc in curseurPsy:
                if 'RGEALTI' in fichierAsc[0]:
                    fichierCompletAsc=os.path.join(dossierEntreRge,fichierAsc[0])#la ligne suivante permet de ne pas conserver les données Rge à -99999 mais le plus simple serait plutot de modifier la création du dallage ene le limitant au zone hors nodata. POur se faire : attribuer une valeur 1 aux nodata, reclassifier le raster en affactant une valeur 0 aux reste, puis polygoniser. cela doit se faire via gdal mais là j'ai pas le temps
                    rqtBuffer='WITH buff_tot_dept(geom) AS (SELECT geom FROM zonage.zone_precision WHERE code_dept=\'%s\'),buff_nodata AS (SELECT CASE WHEN (select exists (SELECT ST_SetSRID(St_Buffer(St_ConvexHull(ST_COllect(ST_MakePoint(x,y,z))),0.50),2154) AS geom FROM topographie.points_cotes WHERE geom IS NULL AND z=-99999 GROUP BY geom))= true THEN (SELECT ST_SetSRID(St_Buffer(St_ConvexHull(ST_COllect(ST_MakePoint(x,y,z))),0.50),2154)  FROM topographie.points_cotes WHERE geom IS NULL AND z=-99999 GROUP BY geom)ELSE ST_GeomFromText(\'POINT(-1 1)\') END::geometry AS geom),buffer_route_a_carto(geom) AS (SELECT CASE WHEN st_astext(n.geom)<>\'POINT(-1 1)\' AND ST_Intersects(dr.geom, b.geom) THEN ST_SetSRID(ST_Difference(ST_Intersection(dr.geom, b.geom),n.geom),2154) ELSE ST_SetSRID(ST_Intersection(dr.geom, b.geom),2154) END::geometry AS geom FROM topographie.dalles_rgealti AS dr, buff_tot_dept AS b, buff_nodata AS n WHERE dr.nom_dalle=\'%s\' AND ST_Intersects(dr.geom, b.geom))'%(codeDept,fichierAsc[0])
                elif 'BDALTI' in fichierAsc[0]:
                    fichierCompletAsc=os.path.join(dossierEntreBdalti,fichierAsc[0])
                    rqtBuffer='with buff_tot_dept_ze AS (SELECT ze.geom FROM zonage.zone_etude AS ze WHERE code_dept=\'%s\'),buff_tot_dept_zp AS (SELECT ST_Buffer(ST_Collect(ST_Intersection(zp.geom,dr.geom)),0.2) AS geom, row_number()over() AS id FROM zonage.zone_precision AS zp, topographie.dalles_rgealti AS dr WHERE code_dept=\'%s\' GROUP BY code_dept),buff_nodata AS (SELECT ST_SetSRID(St_Buffer(St_ConvexHull(ST_COllect(ST_MakePoint(x,y,z))),0.50),2154) AS geom, row_number()over() AS id FROM topographie.points_cotes WHERE geom IS NULL AND z=-99999 GROUP BY geom), buff_tot_dept_zp2 AS (SELECT ST_SetSRID(St_Buffer(St_Collect(ST_Difference(ST_Intersection(dr.geom, b.geom),n.geom)),0),2154) AS geom FROM topographie.dalles_rgealti AS dr, buff_tot_dept_zp AS b, buff_nodata AS n WHERE ST_Intersects(dr.geom, b.geom) AND ST_Intersects(dr.geom, n.geom)),buff_final AS (SELECT CASE WHEN NOT zp2.geom IS NULL AND ST_Intersects(ze.geom, zp2.geom) THEN ST_Difference(ze.geom, zp2.geom) WHEN zp2.geom IS NULL AND NOT zp.geom IS NULL AND ST_Intersects(ze.geom, zp.geom) THEN ST_Difference(ze.geom, zp.geom) ELSE ze.geom END  As geom, row_number()over() AS id FROM buff_tot_dept_ze AS ze, buff_tot_dept_zp2 AS zp2, buff_tot_dept_zp AS zp), buffer_route_a_carto(geom,id) AS ( SELECT ST_SetSRID(ST_Intersection(dr.geom, b.geom),2154) AS geom, row_number()over() FROM topographie.dalles_bdalti AS dr,  buff_final AS b WHERE dr.nom_dalle=\'%s\' AND ST_Intersects(dr.geom, b.geom))'%(codeDept,codeDept,fichierAsc[0])
                    
                if fichierCompletAsc[-4:]!='.asc':
                    print (fichierCompletAsc[-4:])
                    fichierCompletAsc=fichierCompletAsc+'.asc'
                print (fichierCompletAsc)
                fichierXyz=importer.Asc2xyz(fichierCompletAsc)
                curseurPsy2.execute('COPY topographie.points_cotes (x,y,z) FROM \'%s\' DELIMITER \' \''%(fichierXyz))
                connecterBdd.connexionPsy.commit()
                print ('ficher xyz copié dans Bdd')
                try:
                    curseurPsy2.execute('%s UPDATE topographie.points_cotes AS p SET geom=ST_SetSRID(ST_MakePoint(p.x,p.y,p.z),2154),nom_dalle=\'%s\', code_dept=\'%s\'  FROM buffer_route_a_carto AS b WHERE ST_Within(ST_SetSRID(ST_MakePoint(p.x,p.y,p.z),2154), b.geom)'%(rqtBuffer,fichierAsc[0],codeDept))
                    connecterBdd.connexionPsy.commit()
                    curseurPsy2.execute('DELETE FROM topographie.points_cotes WHERE geom IS NULL')
                except : 
                    print ('erreur sur le fichier : ',fichierAsc[0])
                connecterBdd.connexionPsy.commit()
                os.remove(fichierXyz)
                print ('points crées')
        
        BoiteMessage('fin création des points xyz','tout fait')                       
        
def BoiteMessage(titre,texte,typeIcone=QMessageBox.Warning):
    """
    Methode pour creer une boite de message en 1 seule ligne
    """
    msg=QMessageBox()
    msg.setText(texte)
    msg.setWindowTitle(titre)
    msg.setIcon(typeIcone)
    msg.exec_()
                    
if __name__=='__main__':
    app=QApplication(sys.argv)
    test = Topographie()
    test.show()
    sys.exit(app.exec_())