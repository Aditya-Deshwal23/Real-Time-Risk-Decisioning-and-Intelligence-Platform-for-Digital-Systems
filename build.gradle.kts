plugins {
    base
    alias(libs.plugins.spotless) apply false
}

subprojects {
    plugins.apply("base")
    group = "dev.verdict"
}

tasks.named("build") {
    dependsOn(subprojects.map { it.tasks.named("build") })
}
