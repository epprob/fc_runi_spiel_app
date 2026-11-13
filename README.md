# FC Runi App

Begleit-App für das FC-Runi-Spiel: Spieltag berechnen, Teams verwalten, Meisterschaftstabelle.

## Dateien

| Datei | Zweck |
|---|---|
| `main.py` | **Android/Kivy-App** (Einstiegspunkt für Buildozer) |
| `main_desktop.py`, `source/Gui.py` | ursprüngliche Tkinter-Version für den PC |
| `source/game_logic.py` | Spielberechnung (ohne Oberfläche, getestet) |
| `source/store.py` | Speichern/Laden der Teams als JSON |
| `buildozer.spec` | Android-Build-Konfiguration |
| `.github/workflows/build-apk.yml` | baut die APK automatisch bei GitHub |

## APK bauen – Variante A: GitHub Actions (kein Setup nötig)

1. Diese Dateien ins GitHub-Repository übernehmen und pushen.
2. Auf GitHub: **Actions → Build Android APK** (läuft automatisch beim Push, oder „Run workflow").
3. Nach ca. 15–30 Minuten beim fertigen Lauf unter **Artifacts** `fc-runi-apk` herunterladen.
4. APK aufs Handy übertragen und installieren (Installation aus unbekannten Quellen erlauben).

## APK bauen – Variante B: lokal (Linux oder WSL2 unter Windows)

```bash
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config \
  zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev
pip install buildozer cython
buildozer android debug       # erster Build lädt SDK/NDK, dauert lange
# Ergebnis: bin/fcruni-0.1-*-debug.apk
# Direkt aufs angeschlossene Handy: buildozer android debug deploy run
```

## Am PC testen (ohne Android)

```bash
pip install kivy
python main.py            # Kivy-Version
python main_desktop.py    # alte Tkinter-Version
python -m unittest discover -s tests
```
