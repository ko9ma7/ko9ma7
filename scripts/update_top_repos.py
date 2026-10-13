#!/usr/bin/env python3
"""Update the starred-repositories section of the ko9ma7 profile README.

Uses only the Python standard library. Public, original, non-archived repos
are ranked by stargazers_count. Changes are confined to the marked section.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import json

OWNER = "ko9ma7"
TOP_N = 6
MIN_STARS = 0
EXCLUDED_NAMES = {"ko9ma7", "VisionFlow-Studio"}
START = "<!-- TOP_REPOS:START -->"
END = "<!-- TOP_REPOS:END -->"
README = Path(__file__).resolve().parents[1] / "README.md"
API = "https://api.github.com"


def fetch_public_repositories(owner: str = OWNER) -> list[dict]:
    """Fetch all public repositories, stopping only after the last full page."""
    repositories: list[dict] = []
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-top-repositories",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Personal account may contain thousands of repositories. Do not inspect
    # just the first 100: it would produce an incorrect star ranking.
    for page in range(1, 101):
        params = urlencode({"per_page": 100, "page": page, "type": "owner"})
        url = f"{API}/users/{quote(owner)}/repos?{params}"
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                current_page = json.load(response)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f"GitHub API failed on page {page}: {exc}") from exc
        if not isinstance(current_page, list):
            raise RuntimeError(f"Unexpected GitHub API response on page {page}")
        repositories.extend(current_page)
        if len(current_page) < 100:
            return repositories
    raise RuntimeError("More than 10,000 repositories: increase pagination limit")


def select_top_repositories(repositories: list[dict]) -> list[dict]:
    candidates = [
        repo for repo in repositories
        if isinstance(repo, dict)
        and repo.get("name") not in EXCLUDED_NAMES
        and not repo.get("fork", False)
        and not repo.get("archived", False)
        and not repo.get("private", False)
        and repo.get("owner", {}).get("login", "").casefold() == OWNER.casefold()
        and int(repo.get("stargazers_count") or 0) >= MIN_STARS
    ]
    return sorted(
        candidates,
        key=lambda repo: (
            -int(repo.get("stargazers_count") or 0),
            -(int(repo.get("forks_count") or 0)),
            repo.get("name", "").casefold(),
        ),
    )[:TOP_N]


def md_cell(value: object, max_chars: int = 96) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "…"
    # Preserve valid Markdown table structure with arbitrary descriptions.
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("`", "\\`")


def render_repos(repositories: list[dict]) -> str:
    selected = select_top_repositories(repositories)
    if not selected:
        return (
            "소개할 공개 원본 저장소가 아직 없습니다. "
            "[모든 저장소 보기](https://github.com/ko9ma7?tab=repositories)"
        )

    lines = [
        "| 프로젝트 | 소개 | ⭐ Stars | 언어 |",
        "| :-- | :-- | --: | :-- |",
    ]
    for repo in selected:
        name = str(repo["name"])
        label = md_cell(name, 80).replace("[", "\\[").replace("]", "\\]")
        url = f"https://github.com/{OWNER}/{quote(name)}"
        description = md_cell(repo.get("description") or "공개 개발 저장소")
        stars = int(repo.get("stargazers_count") or 0)
        language = md_cell(repo.get("language") or "—", 24)
        lines.append(f"| [**{label}**]({url}) | {description} | **{stars:,}** | {language} |")
    lines.extend([
        "",
        f"<sub>⭐ Star 기준 상위 {len(selected)}개 · Fork/Archived 제외 · VisionFlow Studio는 위에서 별도 소개</sub>",
        "",
        "[📂 모든 공개 저장소 보기](https://github.com/ko9ma7?tab=repositories)",
    ])
    return "\n".join(lines)


def replace_section(content: str, rendered: str) -> str:
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("README requires exactly one TOP_REPOS:START and TOP_REPOS:END marker")
    start_pos = content.index(START) + len(START)
    end_pos = content.index(END)
    if start_pos > end_pos:
        raise ValueError("TOP_REPOS markers are out of order")
    return content[:start_pos] + "\n" + rendered.rstrip() + "\n" + content[end_pos:]


def main() -> int:
    old = README.read_text(encoding="utf-8")
    top = render_repos(fetch_public_repositories())
    new = replace_section(old, top)
    if old == new:
        print("No change in most-starred repositories.")
    else:
        README.write_text(new, encoding="utf-8")
        print("Updated README most-starred repositories.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(f"Failed to update README: {exc}", file=sys.stderr)
        sys.exit(1)
