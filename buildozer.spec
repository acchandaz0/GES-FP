[app]
title = apt-deliver packages
package.name = aptdeliver
package.domain = org.aptdeliver
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1
requirements = python3,kivy

# Android specific
android.permissions = INTERNET
android.api = 29
android.minapi = 21
android.sdk = 29
android.ndk = 21.4.7075529
android.arch = armeabi-v7a

# Orientation
orientation = portrait

# Application entry point
android.entrypoint = src.kivy_main:AptDeliverApp

# Include necessary files
source.include_patterns = assets/*,src/*

# Exclude unnecessary files
source.exclude_dirs = __pycache__,bin,build,dist

# Icon and presplash (you can update these later)
#icon.filename = %(source.dir)s/assets/images/icon.png
#presplash.filename = %(source.dir)s/assets/images/splash.png
