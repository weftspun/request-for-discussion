---
title: "RFD 2048: Android template builds with Temurin JDK 21 and config.gradle-pinned SDK"
rfd: "2048"
state: published
scope: Android export template build toolchain
---

## Problem

The project needs an Android export template of the merged
double-precision assembly for OpenXR builds. The build box carries no
Android SDK. Fedora 44 packages only JDK 25 and 26, and Gradle rejects
Java 25 with an "Unsupported class file major version 69" error.

## Decision

The Android export template of the merged double-precision assembly
is needed for OpenXR builds. The box carries no Android SDK, and
Fedora 44 packages only JDK 25 and 26; Gradle rejects Java 25 with
"Unsupported class file major version 69". The project pins the
Android toolchain to what the fork's
`platform/android/java/app/config.gradle` declares — NDK
`29.0.14206865`, build-tools `36.1.0`, platform `android-36` —
installed through `sdkmanager` from the command-line tools, and runs
Gradle on a Temurin JDK 21 tarball fetched from the Adoptium API,
because the distribution ships no Gradle-compatible JDK and the
tarball pins the version per checkout. The verified sequence: `scons
platform=android target=template_release arch=arm64 precision=double`
produces `libgodot_android.so` (about four minutes on the
workstation), then `JAVA_HOME=<temurin-21> ./gradlew
generateGodotTemplates` produces `bin/android_release.apk`. The
Android OpenXR export template exists before the gate, retiring the
toolchain risk. `config.gradle` is the single source of truth for SDK
versions; reading it first avoids guessing. The JDK is per-user
(`~/jdks`), so system Java stays at the distribution default.

## References

- Original record:
  `decisions/20260612-android-template-temurin-jdk21.md`

## Related

- `rfd/2007-godot-double-precision-template-release-for-zone`: the
  double-precision assembly this template builds from.
