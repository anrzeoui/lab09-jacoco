package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/** Lab09 D: BVA values. Exactly 60 MUST fail with the starter's > 60 bug. */
class ScholarshipCalculatorBoundaryTest {
    private final ScholarshipCalculator calc = new ScholarshipCalculator();

    @Test
    void letterGrade_exactSixty_returnsD() {
        assertEquals("D", calc.letterGrade(60));
    }

    @Test
    void letterGrade_belowSixty_returnsF() {
        assertEquals("F", calc.letterGrade(59.99));
    }

    @Test
    void letterGrade_upperDEdge_returnsD() {
        assertEquals("D", calc.letterGrade(69.99));
    }

    @Test
    void letterGrade_zero_returnsF() {
        assertEquals("F", calc.letterGrade(0));
    }

    @Test
    void letterGrade_hundred_returnsA() {
        assertEquals("A", calc.letterGrade(100));
    }

    @Test
    void letterGrade_belowNinety_returnsB() {
        assertEquals("B", calc.letterGrade(89.99));
    }

    @Test
    void letterGrade_ninety_returnsA() {
        assertEquals("A", calc.letterGrade(90));
    }
}
