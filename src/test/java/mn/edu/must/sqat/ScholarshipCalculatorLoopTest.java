package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/** Lab09 C: 0/1/2+ iterations plus null precondition. */
class ScholarshipCalculatorLoopTest {
    private final ScholarshipCalculator calc = new ScholarshipCalculator();

    @Test
    void gpa_zeroIterations_emptyArray_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(new double[]{}));
    }

    @Test
    void gpa_nullArray_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(null));
    }

    @Test
    void gpa_oneIteration_returnsFour() {
        assertEquals(4.0, calc.gpa(new double[]{95}), 1e-9);
    }

    @Test
    void gpa_manyIterations_returnsTwoPointFive() {
        assertEquals(2.5, calc.gpa(new double[]{95, 85, 75, 65}), 1e-9);
    }
}
