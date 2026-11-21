plugins {
    application
    id("verdict.java-conventions")
}

val catalog = extensions.getByType<VersionCatalogsExtension>().named("libs")
dependencies {
    add("compileOnly", "org.jspecify:jspecify:${catalog.findVersion("jspecify").get().requiredVersion}")
}
