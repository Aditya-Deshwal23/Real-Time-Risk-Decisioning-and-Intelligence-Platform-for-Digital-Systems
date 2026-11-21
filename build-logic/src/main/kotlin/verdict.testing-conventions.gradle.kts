plugins {
    java
}

val catalog = extensions.getByType<VersionCatalogsExtension>().named("libs")
val junitVersion = catalog.findVersion("junit").get().requiredVersion

dependencies {
    add("testImplementation", "org.junit.jupiter:junit-jupiter:$junitVersion")
    add("testRuntimeOnly", "org.junit.platform:junit-platform-launcher:$junitVersion")
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
    reports {
        junitXml.required.set(true)
        html.required.set(true)
    }
}
