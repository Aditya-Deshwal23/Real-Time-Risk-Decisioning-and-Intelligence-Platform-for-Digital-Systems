package io.verdict.stream;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

import org.junit.jupiter.api.Test;

class StreamApplicationTest {

  @Test
  void mainReturnsWithoutStartingTopology() {
    assertDoesNotThrow(() -> StreamApplication.main(new String[0]));
  }
}
