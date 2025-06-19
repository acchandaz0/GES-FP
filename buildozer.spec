[app]
# (str) Title of your application
title = Apt-deliver

# (str) Version of your application
version = 1.0

# (str) Package name
package.name = aptdeliverpackage

# (str) Package domain (needed for android/ios packaging)
package.domain = com.arsya

# (str) custom python-for-android branch to use
p4a.branch = develop

# (str) Source code where the main.py live
source.dir = src

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,otf

# (list) List of modules toனே include in your package
requirements = python3,kivy

# (str) The Android arch to build for, one of armeabi-v7a, arm64-v8a, x86, x86_64
# Google Play requires arm64-v8a
android.arch = arm64-v8a

# (int) Android API to use
android.api = 33

# (str) The Android build tools version to use
android.build_tools_version = 33.0.0

# (str) The Android SDK platform to use
android.sdk_platform = 33

# (int) Minimum API required
android.minapi = 21

# (str) Supported orientation (one of landscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET