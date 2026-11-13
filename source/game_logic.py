"""Reine Spiellogik (ohne Oberfläche), identisch zur Berechnung in der Tk-Version."""


def to_float(text, default=0.0):
    """Wandelt Eingabetext in float um; leere/ungültige Eingaben ergeben `default`."""
    try:
        return float(str(text).strip().replace(",", "."))
    except ValueError:
        return default


def compute_match(off_home, def_home, off_away, def_away, wp_home, wp_away):
    """Berechnet das Endresultat (Tore Heim, Tore Auswärts).

    Angriff und Verteidigung werden jeweils um die Würfelpunkte (WP) des
    Teams erhöht. Tore = eigener Angriff - gegnerische Verteidigung, mindestens 0.
    """
    offence_home = off_home + wp_home
    offence_away = off_away + wp_away
    defence_home = def_home + wp_home
    defence_away = def_away + wp_away

    goals_home = max(offence_home - defence_away, 0)
    goals_away = max(offence_away - defence_home, 0)
    return goals_home, goals_away
