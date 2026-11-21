plugins {
    id("verdict.application-conventions")
    alias(libs.plugins.spring.boot)
}

application {
    mainClass.set("dev.verdict.platform.PlatformApplication")
}

dependencies {
    implementation(platform(libs.spring.boot.bom))
    implementation(libs.spring.boot.webmvc)
    implementation(libs.spring.boot.actuator)
    implementation(project(":libs:contracts"))
    implementation(project(":libs:features"))

    testImplementation(libs.spring.boot.test)
    testImplementation(libs.archunit)
}
