plugins {
    id("verdict.application-conventions")
}

application {
    mainClass.set("io.verdict.simulator.SimulatorApplication")
}

dependencies {
    implementation(project(":libs:contracts"))
}
