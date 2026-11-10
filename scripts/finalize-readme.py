#!/usr/bin/env python3
'''Regenerate README from real local Maven/JaCoCo logs and environment. No fake PASS claims.'''
from pathlib import Path
import subprocess, csv, re, sys
root=Path(__file__).resolve().parent.parent
results=root/'results'
required=['mvn-verify-A.txt','jacoco-A.csv','mvn-verify-B.txt','jacoco-B.csv','mvn-test-D-fail.txt','mvn-verify-final.txt','jacoco-final.csv']
missing=[n for n in required if not (results/n).is_file()]
if missing: sys.exit('ERROR: missing actual results: '+', '.join(missing))

def log(name,expected):
    v=(results/name).read_text(encoding='utf-8',errors='replace')
    v=re.sub(r'\x1b\[[0-9;]*m', '', v)  # tolerate ANSI-colored Maven output
    if expected not in v: sys.exit(f'ERROR: {name}: expected {expected} missing')
    x=re.findall(r'Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)',v)
    if not x: sys.exit(f'ERROR: {name}: no test-count record')
    return v,tuple(map(int,x[-1]))
la,ca=log('mvn-verify-A.txt','BUILD SUCCESS')
lb,cb=log('mvn-verify-B.txt','BUILD SUCCESS')
ld,cd=log('mvn-test-D-fail.txt','BUILD FAILURE')
lf,cf=log('mvn-verify-final.txt','BUILD SUCCESS')
if ca[0]!=5 or any(ca[1:]) or any(cb[1:]) or any(cf[1:]) or cd[1]<1:
    sys.exit('ERROR: unexpected test statistics; inspect logs manually')
if 'letterGrade_exactSixty_returnsD' not in ld:
    sys.exit('ERROR: D fail log does not identify the exact-60 boundary test')

def coverage(name):
    with (results/name).open(encoding='utf-8-sig', newline='') as f:rows=list(csv.DictReader(f))
    rows=[r for r in rows if r.get('CLASS')=='ScholarshipCalculator']
    if len(rows)!=1: sys.exit(f'ERROR: bad CSV record for {name}')
    r=rows[0]
    lines=tuple(int(r[f'LINE_{a}']) for a in ('MISSED','COVERED'))
    branches=tuple(int(r[f'BRANCH_{a}']) for a in ('MISSED','COVERED'))
    def percent(pair):return 100*pair[1]/sum(pair) if sum(pair) else 100
    return lines,branches,percent(lines),percent(branches)
(a_l,a_b,a_lp,a_bp)=coverage('jacoco-A.csv')
(b_l,b_b,b_lp,b_bp)=coverage('jacoco-B.csv')
(f_l,f_b,f_lp,f_bp)=coverage('jacoco-final.csv')
if b_l[0]!=0 or b_b[0]!=0 or f_l[0]!=0 or f_b[0]!=0:
    sys.exit('ERROR: B/final must have LINE_MISSED=0 and BRANCH_MISSED=0')

def output(cmd):
    p=subprocess.run(cmd,cwd=root, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if p.returncode:sys.exit(f'ERROR: command failed: {cmd}\n{p.stdout}')
    # Remove terminal colors from Maven -version
    return re.sub(r'\x1b\[[0-9;]*m','',p.stdout.strip())
java=output(['java','-version']); maven=output(['mvn','-version'])
# Exact exception message may vary; do not paraphrase as observed beyond log line.
errors=[s.strip() for s in ld.splitlines() if ('letterGrade_exactSixty_returnsD' in s and ('FAILURE' in s or 'Failure' in s)) or 'expected: <d>' in s.lower()]
failure_excerpt='\n'.join(errors[:4]) if errors else 'letterGrade_exactSixty_returnsD — FAIL (see results/mvn-test-D-fail.txt)'
readme=f'''# Лаборатори №9 — JaCoCo код хамралт

**Хичээл:** F.CSA313 — Программ хангамжийн чанарын баталгаа ба тест  
**Оюутан:** Ө. Анар  
**Оюутны код:** B242270129  
**Тестийн бай:** `ScholarshipCalculator` (`letterGrade`, `gpa`, `scholarship`)  
**Эх сурвалж:** Багшийн starter project; `pom.xml` өөрчлөгдөөгүй.  
**AI ашиглалт:** Тестүүдийн хувилбар, Maven-ийн лог цуглуулах скрипт, CSV-ээс хамралт гаргах код болон CFG-ийн дижитал лавлах зургийг бэлтгэхэд ChatGPT ашигласан. Үр дүнгийн утга бүрийг өөрийн Maven/JaCoCo логуудаар нягталсан.

## Орчин

`java -version` бүтэн гаралт:

```text
{java}
```

`mvn -version` бүтэн гаралт:

```text
{maven}
```

## Хэсэг A — Happy path, эхний хамралт

Эхний **{ca[0]}** тест ногоон ажилласан. Багшийн starter кодын зориуд алдаатай зааг (`score > 60`) энэ шатанд өөрчлөгдөөгүй. 

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
| Line | {a_l[1]} | {a_l[0]} | **{a_lp:.2f}%** |
| Branch | {a_b[1]} | {a_b[0]} | **{a_bp:.2f}%** |

Эхний 5 happy path тестээр A/B ангилал, эерэг оролттой GPA, тэтгэлэг олгох болон сахилгын зөрчилтэй замууд шалгагдсан. JaCoCo HTML тайлангийн шар ромб нь илэрхийллийн зөвхөн зарим салаа ажилласныг, улаан мөр нь тестээр огт дайраагүй замыг илтгэнэ. Тухайлбал хүчингүй оноо, `null`/хоосон массив, урьдчилсан шалгалтын exception-ийн замууд A шатанд хамрагдаагүй байсан.

Нотолгоо: [`mvn-verify-A.txt`](results/mvn-verify-A.txt), [`jacoco-A.csv`](results/jacoco-A.csv).

## Хэсэг B — CFG ба 100% branch / line

Тэтгэлгийн `scholarship()` функцын CFG-д богино холболттой `||`, `&&` нөхцөл бүрийг тусад нь зангилаа болгон дүрсэлсэн. Ирмэгүүдийн нэр `ScholarshipCalculatorHappyPathTest` эсвэл `ScholarshipCalculatorBranchTest` доторх бодит тестийн методтой таарна. **Анхаар:** `cfg.png` бол дижитал лавлах зураг; багшийн «гараар зур» шаардлагад нийцүүлэхийн тулд үүнийг өөрийн гараар draw.io/цаасан дээр сэргээн зурж зурагтай солих нь зүйтэй.

![Scholarship CFG](cfg.png)

Шат B-д **{cb[0]}** тест амжилттай ажилласан.

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
| Line | {b_l[1]} | {b_l[0]} | **{b_lp:.2f}%** |
| Branch | {b_b[1]} | {b_b[0]} | **{b_bp:.2f}%** |

`letterGrade`-ийн A/B/C/D/F, `gpa`-ийн switch default, `scholarship`-ийн гурван тоон оролтын exception болон `&&`/`||` доторх хоёр дахь нөхцөлүүдийг тусад нь шалгаснаар бүх салаанд хүрсэн. **Энэ шатанд `letterGrade(60)`-ийг хараахан шалгаагүй**, тиймээс зориудын заагийн алдаа тестэд илрээгүй хэвээр байсан.

Нотолгоо: [`mvn-verify-B.txt`](results/mvn-verify-B.txt), [`jacoco-B.csv`](results/jacoco-B.csv).

## Хэсэг C — Давталтын 0 / 1 / 2+ зааг

- **0 давталт** — `gpa_zeroIterations_emptyArray_throws`, `assertThrows`.
- **null оролт** — `gpa_nullArray_throws`, `assertThrows`.
- **1 давталт** — `gpa_oneIteration_returnsFour`, `gpa([95]) = 4.0`.
- **2+ давталт** — `gpa_manyIterations_returnsTwoPointFive`, `gpa([95,85,75,65]) = 2.5`.

Branch хамралт өмнөх шатанд 100% хүрсэн тул эдгээр тестүүд хамралтын хувийг нэмэхгүй байж болно. Гэхдээ давталтын хэмжээ, массивын хоосон нөхцөл болон бүх элемент зөв тоологдохыг хамгаалдаг учир зөвхөн хамралтын хэмжүүрээр илэрхийлэгдэхгүй өгөгдлийн алдааг барихад хэрэгтэй.

## Хэсэг D — 100% coverage ≠ 100% correctness

`letterGrade(60)`-д `"D"` хүлээсэн боловч starter эх кодын `if (score > 60)` нөхцөлөөс болж `"F"` буцсан. Үүнийг `letterGrade_exactSixty_returnsD` тест илрүүлсэн; тухайн үеийн Maven test **{cd[1]} failure**-тай, **BUILD FAILURE** болсон.

```text
{failure_excerpt}
```

Нотолгоо: [`mvn-test-D-fail.txt`](results/mvn-test-D-fail.txt).

Тусдаа засварын үе шатанд `if (score > 60)`-ыг **`if (score >= 60)`** болгож зассан. Сүүлийн `mvn verify`-д **{cf[0]}** тест PASS болсон.

| Хэмжүүр | Covered | Missed | Хамралт |
|---|---:|---:|---:|
| Line | {f_l[1]} | {f_l[0]} | **{f_lp:.2f}%** |
| Branch | {f_b[1]} | {f_b[0]} | **{f_bp:.2f}%** |

Нотолгоо: [`mvn-verify-final.txt`](results/mvn-verify-final.txt), [`jacoco-final.csv`](results/jacoco-final.csv).

**Гол дүгнэлт:** Branch хамралт 100% байсан ч онооны `60` гэсэн заагийн оролтыг шалгаагүй тул буруу харьцуулалтын оператор амьд үлдсэн. `score > 60` болон `score >= 60` нь аль аль нь үнэн/худал салаа үүсгэх учраас хамралтын тайлан уг операторын утгын алдааг шууд илрүүлж чадахгүй. JaCoCo нь кодын аль мөр, салаа ажилласныг хэмждэг болохоос үр дүн нь спецификацитай тохирсон эсэхийг батлахгүй. Харин `letterGrade(60)` гэсэн заагийн тест expected `D` болон actual `F`-ийн зөрүүг барьсан. Иймээс өндөр хамралтыг boundary value analysis, утгын assertion болон алдаа хайх тесттэй хавсарч ашиглах хэрэгтэй.

## Дахин ажиллуулах

```bash
mvn verify
xdg-open target/site/jacoco/index.html
```

`results/` хавтсанд A/B/D/final үе шатын бодит TXT, CSV нотолгоонууд хадгалагдсан. Commit-ууд A (happy path), B (coverage), C (loop), D (BVA), D-fix (операторын засвар) гэсэн үе шат бүрийг тус тусад нь баримтжуулна.
'''
(root/'README.md').write_text(readme,encoding='utf-8')
print('Generated README:', len(readme), 'chars')
