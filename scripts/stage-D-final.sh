#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
if ! command -v mvn >/dev/null; then echo 'ERROR: Maven суулгаагүй байна: sudo apt install maven' >&2; exit 2; fi
echo '=== Lab09 D: fix the > 60 defect and run all tests ==='
if ! test -f results/mvn-test-D-fail.txt; then echo 'ERROR: capture failing log with stage-D-fail.sh first' >&2; exit 2; fi
python3 - <<'PY_FIX'
from pathlib import Path
p=Path('src/main/java/mn/edu/must/sqat/ScholarshipCalculator.java')
s=p.read_text(encoding='utf-8')
old='if (score > 60)  return "D";'
new='if (score >= 60) return "D";'
if old in s:
    if s.count(old)!=1: raise SystemExit('ERROR: unexpected multiple source patterns')
    p.write_text(s.replace(old,new,1),encoding='utf-8')
elif new in s:
    print('Source fix already applied.')
else:
    raise SystemExit('ERROR: expected source code not found; inspect letterGrade()')
PY_FIX
mvn -B -Dstyle.color=never verify 2>&1 | tee results/mvn-verify-final.txt
cp target/site/jacoco/jacoco.csv results/jacoco-final.csv
python3 scripts/check-coverage.py final
