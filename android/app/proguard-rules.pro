# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Google Mobile Ads SDK
-keep class com.google.android.gms.ads.** { *; }
-keep class com.google.android.gms.common.GooglePlayServicesUtil { *; }
-keep class com.google.android.gms.common.GooglePlayServicesRepairableException { *; }
-keep class com.google.android.gms.common.GooglePlayServicesNotAvailableException { *; }
-keep interface com.google.android.gms.ads.** { *; }
-keepattributes *Annotation*,EnclosingMethod

# AdMob custom plugin
-keep class com.jogopulo.vagalume.AdMobPlugin { *; }
-keep class com.jogopulo.vagalume.MainActivity { *; }

# Capacitor
-keep class com.getcapacitor.** { *; }
-keep interface com.getcapacitor.** { *; }
-keepattributes Signature
-keepattributes *Annotation*

# WebView
-keepclassmembers class fqcn.of.javascript.interface.for.webview {
   public *;
}

# Preserve line numbers for debugging
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
