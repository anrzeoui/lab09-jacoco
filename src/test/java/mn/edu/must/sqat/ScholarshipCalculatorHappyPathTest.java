package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/** Lab09 A: five ordinary happy-path tests; deliberately no boundary case at 60. */
class ScholarshipCalculatorHappyPathTest {
    private final ScholarshipCalculator calc = new ScholarshipCalculator();

    @Test
    void letterGrade_highScore_returnsA() {
        assertEquals("A", calc.letterGrade(95));
    }

    @Test
    void letterGrade_middleScore_returnsB() {
        assertEquals("B", calc.letterGrade(85));
    }

    @Test
    void gpa_twoGrades_returnsThreePointFive() {
        assertEquals(3.5, calc.gpa(new double[]{95, 85}), 1e-9);
    }

    @Test
    void scholarship_hundred_returnsHundred() {
        assertEquals(100, calc.scholarship(3.9, 16, false));
    }

    @Test
    void scholarship_violation_returnsZero() {
        assertEquals(0, calc.scholarship(3.9, 16, true));
    }
}
