# ko9ma7 GitHub 프로필 README 적용 방법

이 패키지는 **README.md 하나만 교체하면 바로 적용되는 버전**입니다.
별도의 SVG 파일 업로드나 assets 폴더 생성이 필요하지 않습니다.

## 가장 쉬운 적용 방법

1. 브라우저에서 아래 주소를 엽니다.
   - https://github.com/ko9ma7/ko9ma7/edit/main/README.md
2. 기존 README.md 내용을 **Ctrl+A → Delete**로 전부 지웁니다.
3. 이 패키지의 `README.md`를 열어 내용을 **전부 복사**합니다.
4. GitHub 편집창에 붙여넣습니다.
5. 우측 상단 또는 하단의 **Commit changes...** 를 누릅니다.
6. Commit message는 예를 들어 아래처럼 입력합니다.
   - `Redesign GitHub profile README`
7. 다시 **Commit changes** 를 눌러 저장합니다.
8. https://github.com/ko9ma7 로 이동해 결과를 확인합니다.

## 파일을 직접 업로드하는 방법

README.md 파일 자체를 업로드하고 싶다면:

1. https://github.com/ko9ma7/ko9ma7 로 이동
2. **Add file → Upload files**
3. 이 패키지의 `README.md`를 업로드
4. 기존 README가 있기 때문에 교체 여부를 확인
5. Commit changes

## 이 README가 사용하는 외부 SVG 서비스

- capsule-render: 상단/하단 웨이브 SVG
- readme-typing-svg: 타이핑 애니메이션
- shields.io: 동적 배지
- skillicons.dev: 기술 스택 아이콘
- github-readme-stats: GitHub 통계 카드

따라서 별도의 SVG 파일을 저장소에 넣지 않아도 됩니다.

## 나중에 문구를 수정할 위치

- 상단 이름: `text=ko9ma7`
- 상단 설명: `desc=Computer Vision · Automation · Windows`
- 타이핑 문구: `lines=...`
- About: `## 👋 About` 아래
- 프로젝트: `## 📌 Selected Projects` 아래
- 기술 스택: `## 🛠 Tech Stack` 아래

## 주의

GitHub Readme Stats는 공개 인스턴스의 트래픽 제한 때문에 가끔 이미지를 불러오지 못할 수 있습니다. 그 경우 README 자체 오류는 아닙니다.
