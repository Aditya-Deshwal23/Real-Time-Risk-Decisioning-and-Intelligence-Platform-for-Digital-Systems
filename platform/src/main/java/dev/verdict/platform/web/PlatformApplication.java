package dev.verdict.platform.web;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "dev.verdict.platform")
public class PlatformApplication {

  public static void main(String[] args) {
    SpringApplication.run(PlatformApplication.class, args);
  }
}
