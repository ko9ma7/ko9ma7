# ko9ma7 GitHub 프로필 업데이트 적용 가이드

## 이번 개선에서 변경된 내용

- 대표 프로젝트 링크를 **https://github.com/ko9ma7/VisionFlow-Studio** 로 변경
- 공식 문서 링크를 **https://ko9ma7.github.io/VisionFlow-Studio/** 로 변경
- YoloMacro-Distribution은 Legacy 프로젝트로 분리 소개
- 상단 배너·애니메이션·링크·기술 스택·GitHub 통계 유지/정돈
- **직접 만든 공개 저장소 중 Star 상위 6개를 자동 소개**: Fork, Archived, 프로필 저장소 제외
- GitHub Actions 자동 실행: 최초 업로드 시, 매일 오전 11:17(한국시간), 또는 수동 실행

## 필수: ZIP 안의 파일을 통째로 업로드하세요

기존 `README.md`만 변경하면 디자인은 적용되지만 **인기 저장소 자동 갱신은 동작하지 않습니다.** 반드시 다음 3개 파일을 저장소의 **정확한 경로**에 넣으세요.

```text
ko9ma7 (프로필 저장소의 최상위 폴더)
├── README.md
├── .github/
│   └── workflows/
│       └── update-top-repos.yml
└── scripts/
    └── update_top_repos.py
```

`APPLY-KO.md`와 `tests/` 폴더는 도움말·테스트용으로, 업로드하지 않아도 됩니다.

### 방법 A: Git으로 업로드 (추천)

기존 프로필 저장소를 로컬로 가져온 뒤 이 패키지의 `README.md`, `.github/`, `scripts/`를 프로젝트 최상위 폴더에 복사합니다. 이후 아래 명령을 실행합니다.

```bash
git add README.md .github/workflows/update-top-repos.yml scripts/update_top_repos.py
git commit -m "Improve profile and auto-feature starred repositories"
git push origin main
```

클론 명령이 필요한 경우:

```bash
git clone https://github.com/ko9ma7/ko9ma7.git
cd ko9ma7
```

### 방법 B: 웹에서 직접 파일 생성·편집

1. README: https://github.com/ko9ma7/ko9ma7/edit/main/README.md 를 열고 이번 `README.md` 전체 내용으로 교체한 후 커밋합니다.
2. 프로필 저장소에서 **Add file → Create new file**을 선택하고 이름을 `.github/workflows/update-top-repos.yml`로 입력합니다. 패키지의 동일 파일 내용을 붙여넣고 커밋합니다.
3. 같은 방식으로 `scripts/update_top_repos.py` 파일을 생성하고 내용을 붙여넣고 커밋합니다.
4. 이 파일 3개가 기본 브랜치(main)에 있는지 확인합니다.

## 처음 자동 목록 실행하기

1. https://github.com/ko9ma7/ko9ma7/actions 에서 **Update most-starred repositories** 워크플로를 선택합니다.
2. **Run workflow → Branch: main → Run workflow** 를 누릅니다.
3. 실행이 성공하면 `README.md`의 `⭐ Most Starred Repositories` 표가 Star 순으로 자동 채워집니다.
4. 이후 매일 11:17 KST 전후로 동작합니다. GitHub Actions 스케줄은 플랫폼 사정에 따라 지연될 수 있습니다.

업로드 커밋 후 자동 실행될 수 있으므로, 이미 목록이 만들어졌다면 수동 실행은 필요하지 않습니다.

## 만약 실행 권한 오류가 난다면

- https://github.com/ko9ma7/ko9ma7/settings/actions 로 이동합니다.
- **General → Workflow permissions** 에서 **Read and write permissions** 를 허용할 수 있는지 확인합니다. 조직/계정 정책에 따라 옵션이 제한될 수 있습니다.
- GitHub Actions가 활성화되어 있는지 확인합니다.
- Branch protection/ruleset 때문에 Actions의 `git push`가 거부되면 규칙에 맞춘 PR 방식으로 조정해야 합니다.
- 공개 저장소의 예약 실행은 장기간 활동이 없으면 비활성화될 수 있어 Actions 설정에서 다시 켜야 할 수 있습니다.

**개인 액세스 토큰(PAT)을 별도로 만들 필요는 없습니다.** 내장된 `GITHUB_TOKEN`을 사용합니다.

## 순위 집계 기준 / 변경 방법

- 공개 저장소만 사용하며 비공개 코드는 조회하거나 공개하지 않습니다.
- 직접 소유한 **원본** 프로젝트만 포함합니다(포크 제외).
- 보관된 저장소, `ko9ma7` 프로필 저장소, 상단에 별도로 소개된 `VisionFlow-Studio`는 제외됩니다.
- Star가 1개 이상인 저장소 중 Star 내림차순, 동점 시 Fork 수 내림차순, 마지막으로 저장소 이름순입니다.
- 표시 개수를 늘리려면 `scripts/update_top_repos.py`의 `TOP_N = 6`을 수정하세요.
- Star 기준 하한을 바꾸려면 `MIN_STARS = 1`을 수정하세요.
- 갱신 시간을 바꾸려면 `.github/workflows/update-top-repos.yml`의 `cron` 값을 UTC 기준으로 변경하세요.
- **README에 있는 `<!-- TOP_REPOS:START -->`, `<!-- TOP_REPOS:END -->` 마커를 삭제하면 자동 생성이 중단됩니다.**

## GitHub에서 직접 고정하는 Pinned 영역은 별개입니다

프로필 하단의 GitHub 기본 `Pinned` 영역은 최대 6개를 수동 지정합니다. README 내 자동 목록은 이 영역을 자동 수정하지 않습니다. 고정 저장소를 바꾸려면 https://github.com/ko9ma7 의 **Customize your pins** 를 사용하세요.

## 사전 테스트 / 외부 서비스

컴퓨터에 Python 3가 설치돼 있으면 아래 명령으로 비네트워크 테스트를 실행할 수 있습니다.

```bash
python -m unittest discover -s tests -v
```

GitHub 통계·타이핑 배너·아이콘은 기존과 같이 외부 이미지 서비스에 의존하므로 일시적으로 표시되지 않을 수 있습니다. 인기 저장소 목록은 GitHub Actions가 생성한 정적 Markdown 표이므로, 외부 이미지 서비스 상태와 무관하게 보입니다.

**현재 이 ZIP 파일 자체가 사용자의 GitHub에 자동 반영된 것은 아닙니다.** 파일을 올리고 커밋해야 프로필에 반영됩니다.
