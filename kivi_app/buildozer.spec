[app]
# Application title
title = Drone Controller App

# Package name
package.name = dronecontroller

# Package domain
package.domain = org.test

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 0.1

# Application requirements
requirements = python3,kivy,requests,urllib3,charset_normalizer,chardet,idna,kivymd

# Supported orientations
orientation = landscape

# List of permissions
android.permissions = INTERNET

# Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# Enable AndroidX support
android.enable_androidx = True

# Minimum Android API level
android.minapi = 21

# Allow backup on Android
android.allow_backup = True

# Log level for buildozer
log_level = 2

[buildozer]
# Log level
log_level = 2

# Display warning if run as root
warn_on_root = 1
