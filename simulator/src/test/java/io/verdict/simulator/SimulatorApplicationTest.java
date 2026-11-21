package io.verdict.simulator;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

import org.junit.jupiter.api.Test;

class SimulatorApplicationTest {

  @Test
  void mainReturnsWithoutGeneratingTraffic() {
    assertDoesNotThrow(() -> SimulatorApplication.main(new String[0]));
  }
}
