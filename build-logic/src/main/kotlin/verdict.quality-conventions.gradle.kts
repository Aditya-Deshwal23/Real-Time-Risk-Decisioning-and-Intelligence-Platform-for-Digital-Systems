import com.github.spotbugs.snom.SpotBugsTask
import org.gradle.api.artifacts.VersionCatalogsExtension

plugins {
    checkstyle
    com.diffplug.spotless
    com.github.spotbugs
    de.thetaphi.forbiddenapis
}

val catalog = extensions.getByType<VersionCatalogsExtension>().named("libs")

checkstyle {
    toolVersion = catalog.findVersion("checkstyle").get().requiredVersion
    configFile = rootProject.file("build-logic/config/checkstyle.xml")
}

spotless {
    java {
        googleJavaFormat(catalog.findVersion("google-java-format").get().requiredVersion)
    }
}

spotbugs {
    toolVersion.set(catalog.findVersion("spotbugs").get().requiredVersion)
    ignoreFailures.set(false)
}

forbiddenApis {
    bundledSignatures.add("jdk-system-out")
    signaturesFiles = files(rootProject.file("build-logic/forbidden-apis.txt"))
}

tasks.withType<SpotBugsTask>().configureEach {
    reports.create("html") {
        required.set(true)
    }
}
