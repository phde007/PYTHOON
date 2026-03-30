# programme d'intérêt général : fournit le prochain index libre pour une zone
# évite une gestion compliquée des index de lignes dans les frames utilisant grid
def next_free_row(container):
    """
    Retourne le prochain index de ligne libre dans un container grid.
    """
    rows = []
    for w in container.grid_slaves():
        info = w.grid_info()
        r = info.get("row")
        if r is not None:
            rows.append(r)
    return 0 if not rows else max(rows) + 1

# Autre fonction d'intérêt général : calculer une couleur de contraste (noir ou blanc) pour un fond donné
def good_contrast_font_color(bg_color):
    bg_color = bg_color.lstrip('#')
    try:
        # On extrait les composantes RGB
        r = int(bg_color[0:2], 16)
        g = int(bg_color[2:4], 16)
        b = int(bg_color[4:6], 16)
        # Formule de luminance perçue
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "black" if luminance > 0.5 else "white"
    except Exception:
        return "white"

#  test de la fonction de contraste
def contrast_choice(bg_color, light_color="#ffffff", dark_color="#000000"):
    """
    Détermine, pour un fond donné, quelle teinte utiliser :
    `light_color` si la couleur de fonte de contraste calculée par
    good_contrast_font_color est « white », sinon `dark_color`.

    bg_color : chaîne hexadécimale de la forme "#rrggbb" ou "rrggbb"
    light_color / dark_color : couleurs retournées selon le cas.
    """
    # on récupère la couleur de texte de contraste
    font = good_contrast_font_color(bg_color)
    # si la fonction a jugé que du blanc est nécessaire, on renvoie
    # la teinte claire, sinon la teinte foncée
    # print (f"Pour le fond {bg_color}, la couleur de contraste est {font}. On choisit {light_color if font == 'white' else dark_color}.")
    return light_color if font == "white" else dark_color


contrast_choice("#AA9EAC")
contrast_choice("#080111")