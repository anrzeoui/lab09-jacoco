#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
if ! command -v mvn >/dev/null; then echo 'ERROR: Maven суулгаагүй байна: sudo apt install maven' >&2; exit 2; fi
echo '=== Lab09 A: 5 happy-path tests, code UNMODIFIED ==='
if test -e src/test/java/mn/edu/must/sqat/ScholarshipCalculatorBranchTest.java; then echo 'ERROR: B tests already added; A must be run before B.' >&2; exit 2; fi
mvn -B -Dstyle.color=never verify 2>&1 | tee results/mvn-verify-A.txt
cp target/site/jacoco/jacoco.csv results/jacoco-A.csv
python3 scripts/check-coverage.py A
