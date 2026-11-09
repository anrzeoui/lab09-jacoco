#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
if ! command -v mvn >/dev/null; then echo 'ERROR: Maven суулгаагүй байна: sudo apt install maven' >&2; exit 2; fi
echo '=== Lab09 C: loop tests 0,1,2+ ==='
if ! test -f results/jacoco-B.csv; then echo 'ERROR: run stage-B.sh first' >&2; exit 2; fi
cp stages/C/ScholarshipCalculatorLoopTest.java src/test/java/mn/edu/must/sqat/
mvn -B -Dstyle.color=never test 2>&1 | tee results/mvn-test-C.txt
