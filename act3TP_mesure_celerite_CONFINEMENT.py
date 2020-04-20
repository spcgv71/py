"""
Sound celerity measurement with arduino
Ultrasonic Ranger v2.0 is connected on arduino digital 7
Be aware of the COM number (PORT_COM variable)
"""
__author__ = "Stéphane BEARNAIS-BARBRY"
__copyright__ = "Copyright 2020, ILC"
__credits__ = ["Stéphane BEARNAIS-BARBRY"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Stéphane BEARNAIS-BARBRY"
__email__ = "sbearnais-barb@ac-dijon.fr"
__status__ = "Released"

import serial, time
import tkinter as tk
from numpy import mean, array, rint, round_
import matplotlib

NMEASURES = 10

# Fonction de gestion des objets graphiques du programme
# Consulter le fichier original pour développer le code (pour les passionné.e.s)
def gui():
    """
    Graphiques : mis dans une fonction pour ne pas allourdir le code
    :return:
    """
    # Taille de la fenêtre
    ROOT.attributes('-fullscreen', True)
    frm_height = ROOT.winfo_screenheight()
    frm_width = ROOT.winfo_screenwidth()
    # Affichage des fenêtres
    frm_mesure = tk.Frame(ROOT, width=frm_width, height=2*frm_height/3)
    frm_mesure.grid_propagate(0)
    frm_mesure.grid(row=0, column=0)
    frm_btn = tk.Frame(ROOT, width=frm_width, height=frm_height/3)
    frm_btn.grid_propagate(0)
    frm_btn.grid(row=1, column=0)
    # Widgets
    lbl_mesure = tk.Label(frm_mesure, text='---', font=('Times', '150', 'bold'), justify=tk.CENTER)
    lbl_mesure.grid_propagate(0)
    lbl_mesure.place(in_=frm_mesure, anchor='c', relx=.5, rely=.5)
    bouton_mesure = tk.Button(frm_btn, text='MESURE', bg='red', font=('Times', '50', 'bold'), justify=tk.CENTER)
    bouton_mesure.place(in_=frm_btn, anchor='c', relx=.5, rely=.5)
    bouton_mesure.config(command=lambda x=NMEASURES: fonctionB(x))
    return lbl_mesure
# Fonction de communication avec le microntrôleur
# Consulter le fichier original pour développer le code (pour les passionné.e.s)
def connection_arduino(port):
    """
    Connexion à l'arduino
    :param port: port de communication sur lequel est branché l'arduino (attention: peut dépendre des ordinateurs utilisés)
    :return: objet serial_port
    """
    if not port:
        for i in [j+3 for j in range(7)]:
            try:
                serial_port = serial.Serial(port='COM'+str(i), baudrate=9600)
                serial_port.close()
                print('le Port COM'+str(i)+" sera utilisé.")
                return 'COM'+str(i)
            except serial.serialutil.SerialException as erreur:
                print('le Port COM'+str(i)+" n'est pas utilisable.")
            except Exception as erreur:
                print('Unkonw Exception occurs : ', erreur)
    else:
        serial_port = serial.Serial(port=port, baudrate=9600)
        serial_port.setDTR(False)
        time.sleep(0.1)
        serial_port.setDTR(True)
        serial_port.flushInput()
        return serial_port

# Fonctions utiles à la physique
def fonctionB(nmesures=1):
    """
    Average measure of NMEASURES
    :param distance: entry contenant la distance entre émetteur & écran
    :param nmesures: nombre de mesures à effectuer pour une distance
    :return duree: moyenne des durées mesurées
    """
    serial_port = connection_arduino(PORT_COM)
    durees = list()
    while len(durees) < nmesures:
        duree = serial_port.readline().split()[0]
        durees.append(int(duree))
    # Affichage de la moyenne arrondi à 0,1 ms des durées mesurées
    durees = [i*1e-3 for i in durees]
    LBL_MESURE.config(text=str(round_(mean(durees), 2))+' ms')
    serial_port.close()
    return

############!!!!!!!!!!!!!!!!!!!!!!!!!######################
# Port com utilisé par l'arduino (à trouver dans gestionnaire de périphériques/Ports (COM et LPT)
PORT_COM = 'COM9'
############!!!!!!!!!!!!!!!!!!!!!!!!!######################

# Listes rassemblant les mesures : deux listes pour le graphique
DISTANCES = list()
DUREES = list()

ROOT = tk.Tk()
ROOT.title("Mesure d'un aller-retour parcouru par une onde ultrasonore entre la source et un écran")
LBL_MESURE = gui()

ROOT.mainloop()
