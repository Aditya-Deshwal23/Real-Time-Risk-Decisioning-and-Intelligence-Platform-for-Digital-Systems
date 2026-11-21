plugins {
    `java-library`
    id("verdict.java-conventions")
}

val catalog = extensions.getByType<VersionCatalogsExtension>().named("libs")
dependencies {
    add("compileOnlyApi", "org.jspecify:jspecify:${catalog.findVersion("jspecify").get().requiredVersion}")
}
