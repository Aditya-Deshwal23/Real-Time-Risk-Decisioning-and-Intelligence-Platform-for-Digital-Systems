import net.ltgt.gradle.errorprone.errorprone

plugins {
    java
    net.ltgt.errorprone
    id("verdict.quality-conventions")
    id("verdict.testing-conventions")
}

val catalog = extensions.getByType<VersionCatalogsExtension>().named("libs")
val javaVersion = catalog.findVersion("java").get().requiredVersion.toInt()
val errorProneVersion = catalog.findVersion("errorprone").get().requiredVersion
val nullAwayVersion = catalog.findVersion("nullaway").get().requiredVersion

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(javaVersion))
}

dependencies {
    add("errorprone", "com.google.errorprone:error_prone_core:$errorProneVersion")
    add("errorprone", "com.uber.nullaway:nullaway:$nullAwayVersion")
}

dependencyLocking {
    lockAllConfigurations()
}

tasks.withType<JavaCompile>().configureEach {
    options.release.set(javaVersion)
    options.compilerArgs.addAll(listOf("-Xlint:all", "-Werror"))
    options.errorprone {
        option("NullAway:OnlyNullMarked", "true")
        option("NullAway:JSpecifyMode", "true")
        error("NullAway")
    }
}
