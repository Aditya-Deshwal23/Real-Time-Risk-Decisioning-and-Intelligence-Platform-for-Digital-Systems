plugins {
    id("verdict.library-conventions")
}

val runtimeClasspath = configurations.named("runtimeClasspath")
val verifyNoRuntimeDependencies = tasks.register("verifyNoRuntimeDependencies") {
    group = "verification"
    description = "Fails if the shared feature library has runtime dependencies."
    doLast {
        val dependencies = runtimeClasspath.get().allDependencies
        check(dependencies.isEmpty()) {
            "libs:features must not have runtime dependencies, but found: " +
                dependencies.joinToString { "${it.group}:${it.name}:${it.version}" }
        }
    }
}

tasks.named("check") {
    dependsOn(verifyNoRuntimeDependencies)
}
