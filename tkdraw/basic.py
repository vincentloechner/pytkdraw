"""Interface graphique basée sur tkinter, non événementielle.

Ce module fournit quatre fonctions élémentaires décrites ci-dessous, pour :
- ouvrir une fenêtre,
- afficher un pixel dans la fenêtre,
- rafraichir la fenêtre,
- attendre sa fermeture.

Si une précondition de ces fonctions n'est pas vérifiée, le programme
s'arrête brutalement avec une erreur de type "AssertionError"

Copyright 2019-2020, Vincent Loechner <loechner@unistra.fr>
Distribué sous licence MIT
"""

# import tkinter as tk
# import queue
import tkdraw.screen as tkd


"""fengra (global): objet de la version simplifiée de cette bibliothèque."""
fengra = None


def ouvre_fenetre(hauteur, largeur):
    """Ouvre une fenêtre graphique.

    Paramètres :
    - hauteur, largeur (entiers) : taille de la fenêtre en pixels
    Préconditions :
    - la fenêtre ne peut être ouverte qu'une seule fois, mais si vous la
    fermez (avec attend_fenetre() dans votre programme), vous pouvez en
    rouvrir une nouvelle
    """
    # initialise la variable globale fengra utilisée dans les autres fonctions
    global fengra
    assert fengra is None, "ERREUR : la fonction ouvre_fenetre() a été appelée\
 plus d'une fois dans votre programme!"
    fengra = tkd.screen((hauteur, largeur), 1, grid=False)


def plot(ligne, colonne, couleur="black"):
    """Affiche un pixel en position (ligne, colonne).

    Remarque : l'affichage n'est vraiment effectué à l'écran qu'après appel
    de la fonction refresh().
    Paramètres :
    - ligne, colonne (entiers): position du pixel à afficher dans la fenêtre
    - couleur (paramètre optionnel, chaîne de caractères) : une couleur
      tkinter. La couleur par défaut est le noir.
      Cet argument est une chaîne de caractère représentant une couleur valide
      de la bibliothèque tkinter. Voir par exemple :
      http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
      On peut aussi spécifier un code RGB, par exemple "#FF0000" -> rouge.
    Préconditions :
    - la fenêtre doit avoir été ouverte précédemment : la fonction
      ouvre_fenetre(hauteur, largeur) doit avoir été appelée
    - 0 <= ligne < hauteur
    - 0 <= colonne < largeur
    """
    assert fengra, "ERREUR : la fonction ouvre_fenetre() n'a pas été appelée !"
    fengra.draw_tile((ligne, colonne), color=couleur, refresh=False)


def refresh():
    """Rafraîchit la fenêtre graphique.

    Tous les plot() appelés précédemment sont affichés à l'écran.
    Précondition :
    - la fenêtre doit avoir été ouverte précédemment : la fonction
      ouvre_fenetre() doit avoir été appelée
    """
    assert fengra, "ERREUR : la fonction ouvre_fenetre() n'a pas été appelée !"
    fengra.refresh()


def attend_fenetre():
    """Attend que l'utilisateur ferme la fenêtre graphique.

    L'utilisateur peut quitter en fermant la fenêtre grâce au bouton de son
    environnement graphique, ou en appuyant la touche 'esc' ou 'q'.
    Remarque : si vous n'appelez pas cette fonction avant la fin de votre
    programme, la fenêtre se ferme automatiquement lorsqu'il s'arrête.
    Précondition :
    - la fenêtre doit avoir été ouverte précédemment : la fonction
      ouvre_fenetre() doit avoir été appelée
    """
    global fengra

    assert fengra, "ERREUR : la fonction ouvre_fenetre() n'a pas été appelée !"
    fengra.refresh()
    while True:
        p = fengra.wait_event()
        if p[0] == "END":
            # si l'utilisateur ferme la fenêtre je quitte
            break
        if p[0] == "key" and (p[1] == "Escape" or p[1] == "q"):
            # si l'utilisateur appuie la touche <esc> ou <q> idem
            break
    fengra.close()
    fengra = None
