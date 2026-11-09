#!/usr/bin/env python3
"""Parse authentic JaCoCo data for ScholarshipCalculator; never fabricate coverage."""
import csv, sys, pathlib, re
stage=sys.argv[1] if len(sys.argv)>1 else 'final'
path=pathlib.Path(f'results/jacoco-{stage}.csv')
if not path.exists(): sys.exit(f'ERROR: missing {path}')
with path.open(newline='',encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
rows=[r for r in rows if r.get('CLASS')=='ScholarshipCalculator']
if len(rows)!=1: sys.exit(f'ERROR: expected one ScholarshipCalculator row; found {len(rows)}')
r=rows[0]
for kind in ('LINE','BRANCH','INSTRUCTION'):
    missed=int(r[f'{kind}_MISSED']); covered=int(r[f'{kind}_COVERED'])
    total=missed+covered
    print(f'{kind}: covered={covered}, missed={missed}, total={total}, percent={100*covered/total if total else 100:.2f}%')
if stage in ('B','final'):
    if int(r['BRANCH_MISSED'])!=0 or int(r['LINE_MISSED'])!=0:
        sys.exit('ERROR: branch or line coverage not 100%; add missing-path test(s), rerun stage.')
    print('PASS: 100% LINE and BRANCH coverage confirmed by CSV.')
