package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/** Lab09 B: complete structural branch/line coverage without testing exact boundary 60. */
class ScholarshipCalculatorBranchTest {
    private final ScholarshipCalculator calc = new ScholarshipCalculator();

    @Test
    void letterGrade_negative_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.letterGrade(-0.01));
    }

    @Test
    void letterGrade_overHundred_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.letterGrade(100.01));
    }

    @Test
    void letterGrade_gradeC_returnsC() {
        assertEquals("C", calc.letterGrade(75));
    }

    @Test
    void letterGrade_gradeD_returnsD() {
        assertEquals("D", calc.letterGrade(65));
    }

    @Test
    void letterGrade_gradeF_returnsF() {
        assertEquals("F", calc.letterGrade(50));
    }

    @Test
    void gpa_allSwitchArms_includingDefault() {
        assertEquals(2.0, calc.gpa(new double[]{95, 85, 75, 65, 50}), 1e-9);
    }

    @Test
    void gpa_null_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(null));
    }

    @Test
    void gpa_empty_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.gpa(new double[]{}));
    }

    @Test
    void scholarship_negativeGpa_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(-0.1, 16, false));
    }

    @Test
    void scholarship_aboveFour_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(4.1, 16, false));
    }

    @Test
    void scholarship_negativeCredits_throws() {
        assertThrows(IllegalArgumentException.class, () -> calc.scholarship(3.5, -1, false));
    }

    @Test
    void scholarship_topGpaCreditsFourteen_returnsSeventy() {
        assertEquals(70, calc.scholarship(3.9, 14, false));
    }

    @Test
    void scholarship_midTier_returnsSeventy() {
        assertEquals(70, calc.scholarship(3.5, 12, false));
    }

    @Test
    void scholarship_midGpaCreditsEleven_returnsFifty() {
        assertEquals(50, calc.scholarship(3.5, 11, false));
    }

    @Test
    void scholarship_lowTier_returnsFifty() {
        assertEquals(50, calc.scholarship(3.2, 15, false));
    }

    @Test
    void scholarship_lowGpa_returnsZero() {
        assertEquals(0, calc.scholarship(2.9, 20, false));
    }

    @Test
    void scholarship_highGpaTooFewCredits_returnsFifty() {
        assertEquals(50, calc.scholarship(3.9, 11, false));
    }
}
