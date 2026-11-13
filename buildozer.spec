[app]
title = FC Runi
package.name = fcruni
package.domain = org.fcruni

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests,bin,.buildozer,.git,.github,__pycache__
source.exclude_patterns = main_desktop.py,source/Gui.py

version = 0.1

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
