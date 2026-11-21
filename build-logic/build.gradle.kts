plugins {
    `kotlin-dsl`
}

dependencies {
    implementation("com.diffplug.spotless:com.diffplug.spotless.gradle.plugin:${libs.versions.spotless.get()}")
    implementation("com.github.spotbugs:com.github.spotbugs.gradle.plugin:${libs.versions.spotbugsPlugin.get()}")
    implementation("net.ltgt.errorprone:net.ltgt.errorprone.gradle.plugin:${libs.versions.errorpronePlugin.get()}")
    implementation("de.thetaphi.forbiddenapis:de.thetaphi.forbiddenapis.gradle.plugin:${libs.versions.forbiddenApis.get()}")
}

dependencyLocking {
    lockAllConfigurations()
}
