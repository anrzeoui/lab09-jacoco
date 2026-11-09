#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
if ! command -v mvn >/dev/null; then echo 'ERROR: Maven суулгаагүй байна: sudo apt install maven' >&2; exit 2; fi
echo '=== Lab09 B: branch coverage, without boundary-60 test ==='
if ! test -f results/jacoco-A.csv; then echo 'ERROR: run stage-A.sh first' >&2; exit 2; fi
cp stages/B/ScholarshipCalculatorBranchTest.java src/test/java/mn/edu/must/sqat/
mvn -B -Dstyle.color=never verify 2>&1 | tee results/mvn-verify-B.txt
cp target/site/jacoco/jacoco.csv results/jacoco-B.csv
python3 scripts/check-coverage.py B
