#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
if ! command -v mvn >/dev/null; then echo 'ERROR: Maven суулгаагүй байна: sudo apt install maven' >&2; exit 2; fi
echo '=== Lab09 D: detect boundary bug (expected BUILD FAILURE) ==='
if ! test -f src/test/java/mn/edu/must/sqat/ScholarshipCalculatorLoopTest.java; then echo 'ERROR: run stage-C.sh first' >&2; exit 2; fi
if grep -q 'if (score >= 60)' src/main/java/mn/edu/must/sqat/ScholarshipCalculator.java; then echo 'ERROR: bug already fixed; D FAIL log must be captured first' >&2; exit 2; fi
cp stages/D/ScholarshipCalculatorBoundaryTest.java src/test/java/mn/edu/must/sqat/
set +e
mvn -B -Dstyle.color=never test 2>&1 | tee results/mvn-test-D-fail.txt
status=${PIPESTATUS[0]}
set -e
if [[ $status -eq 0 ]]; then echo 'ERROR: D boundary test unexpectedly passed. Check source and test.' >&2; exit 1; fi
if ! grep -q 'letterGrade_exactSixty_returnsD' results/mvn-test-D-fail.txt; then echo 'ERROR: failure did not name the expected boundary test' >&2; exit 1; fi
if ! grep -q 'BUILD FAILURE' results/mvn-test-D-fail.txt; then echo 'ERROR: failed Maven build not recorded' >&2; exit 1; fi
echo 'PASS: boundary defect detected. Now fix source in a DIFFERENT commit with stage-D-final.sh.'
