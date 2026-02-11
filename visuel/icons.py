# module icons.py
# definition des icônes utilisées dans l'application

from PIL import Image
import customtkinter as ctk

ICON_SIZE = (28, 28)

ICON_OPEN = ctk.CTkImage(
    light_image=Image.open(r".\images\chevron_bas.png"),
    dark_image=Image.open(r".\images\chevron_bas.png"),
    size=ICON_SIZE)

ICON_CLOSED = ctk.CTkImage(
    light_image=Image.open(r".\images\chevron_droite.png"),
    dark_image=Image.open(r".\images\chevron_droite.png"),
    size=ICON_SIZE
)
