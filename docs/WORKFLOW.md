# Lab09 — үе шат бүрийг тусдаа хийх заавар

Энэ архив нь **ажиллуулахад бэлэн эх код, тестийн шатлал, CSV/log-ийг бодитоор цуглуулах скриптүүд** агуулна. **`results/`-д байгаа `.gitkeep`-ээс өөр файл бол тестээр гаргасан бодит нотолгоо** байх ёстой. Энд Maven/JaCoCo ажиллуулаагүй учраас хуурамч үр дүн нэмээгүй.

## Суурь

```bash
cd ~/Desktop/lab09-jacoco
java -version
mvn -version
```

## А — 5 happy-path тест

```bash
bash scripts/stage-A.sh
# Open the generated report if desired
xdg-open target/site/jacoco/index.html
# Initialize GitHub repository, then commit stage A
[ -d .git ] || git init -b main
git add pom.xml .gitignore README.md src/main src/test scripts docs cfg.png results/mvn-verify-A.txt results/jacoco-A.csv results/.gitkeep
git commit -m 'test(A): happy paths and first JaCoCo coverage'
```

`stages/` хавтасны ирээдүйн тестүүдийг A commit-д нэмэхгүй. `src/test`-д зөвхөн тухайн үеийн тестүүд, `results/`-д жинхэнэ лог орно. Шат бүр дараа нь тусдаа commit хийгдэнэ.

## B — 100% Line/Branch

```bash
bash scripts/stage-B.sh
# Results must say: PASS: 100% LINE and BRANCH coverage confirmed by CSV
git add src/test/java/mn/edu/must/sqat/ScholarshipCalculatorBranchTest.java results/mvn-verify-B.txt results/jacoco-B.csv cfg.png
git commit -m 'test(B): reach 100 percent JaCoCo branch and line coverage'
```

**cfg.png:** Хавсаргасан зураг бол дижитал лавлах. Зангилаа/ирмэгийн бүх утга, тестийн нэрийг ашиглан **өөрийн гараар зураад** `cfg.png` файлыг сольж B commit-д хийвэл багшийн шалгуурыг илүү ягштал хангана.

## C — 0 / 1 / 2+ loop

```bash
bash scripts/stage-C.sh
git add src/test/java/mn/edu/must/sqat/ScholarshipCalculatorLoopTest.java results/mvn-test-C.txt
git commit -m 'test(C): cover loop boundaries zero one many and null'
```

## D — алдааг засахын ӨМНӨ Fail нотолгоо

```bash
bash scripts/stage-D-fail.sh
# Normal outcome: BUILD FAILURE because score=60 is expected D but code returns F
git add src/test/java/mn/edu/must/sqat/ScholarshipCalculatorBoundaryTest.java results/mvn-test-D-fail.txt
git commit -m 'test(D): expose exact-60 boundary defect'
```

## D — алдааг тусдаа commit-д засах + PASS

```bash
bash scripts/stage-D-final.sh
# Check actual CSV missed counts are both zero
git add src/main/java/mn/edu/must/sqat/ScholarshipCalculator.java results/mvn-verify-final.txt results/jacoco-final.csv
git commit -m 'fix(D): change score > 60 to >= 60 per specification'
python3 scripts/finalize-readme.py
git add README.md
git commit -m 'docs: publish Lab09 measured coverage and conclusions'
```

## GitHub

```bash
# First create a PUBLIC repository lab09-jacoco on GitHub,
# then run (only once):
git remote add origin https://github.com/anrzeoui/lab09-jacoco.git
git push -u origin main
```

If origin already exists, use `git push origin main`. Check `git status`, public repository content, and Teams Turn in separately. If `stage-B.sh` reports less than 100%, do not fake CSV or README: inspect JaCoCo HTML to add missing test cases.
