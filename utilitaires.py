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