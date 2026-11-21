plugins {
    id("verdict.application-conventions")
}

application {
    mainClass.set("io.verdict.stream.StreamApplication")
}

dependencies {
    implementation(project(":libs:contracts"))
    implementation(project(":libs:features"))
}
