"""
Module contenant les briques élémentaires utilisées hors du contexte des zones, étant donc à la base 
du programme principal
"""
import Brique as brq
import visuel.constantes_couleurs as cv

def references_documentaires(self, ctrl_frame):
    tbric = brq.Brique(ctrl_frame, "Références règlementaires", couleur_header=cv.BRICK_HEADER_BG, couleur_panneau=cv.BRICK_PANEL_BG) 
