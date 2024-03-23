from collections.abc import Generator
from pathlib import Path
from typing import Self

from _pytest.fixtures import FixtureRequest
import pytest

from icebreaker.versioning import VersionFileBased


@pytest.fixture(scope="function")
def version_file_name() -> str:
    name: str = "version"
    return name


@pytest.fixture(scope="function")
def git_root() -> Generator[Path, None, None]:
    git_root: Path = Path(__file__).parent.parent
    git_dir: Path = git_root / ".git"
    git_dir.mkdir(exist_ok=False)
    yield git_root
    git_dir.rmdir()


@pytest.fixture(scope="function")
def version_file_in_current_dir(version_file_name: str) -> Generator[Path, None, None]:
    version_file: Path = Path(__file__).parent / version_file_name
    version_file.touch(exist_ok=False)
    yield version_file
    version_file.unlink(missing_ok=False)


@pytest.fixture(scope="function")
def version_file_in_git_root(
    version_file_name: str,
    git_root: Path,
) -> Generator[Path, None, None]:
    version_file: Path = git_root / version_file_name
    version_file.touch(exist_ok=False)
    yield version_file
    version_file.unlink(missing_ok=False)


class TestResolveVersion:
    @pytest.mark.parametrize(
        "version_file_fixture",
        [
            "version_file_in_current_dir",
            "version_file_in_git_root",
        ],
    )
    def test_discovers_version(
        self: Self,
        request: FixtureRequest,
        version_file_fixture: str,
    ) -> None:
        # Request the fixture dynamically based on the parameter
        version_file: Path = request.getfixturevalue(version_file_fixture)
        version: str = "1.0.0"
        version_file.write_text(version)
        resolved_version: str = VersionFileBased(version_file_name=version_file.name).resolve_version()
        assert resolved_version == version

    def test_deals_with_whitespace(
        self: Self,
        version_file_in_current_dir: Path,
    ) -> None:
        version_file: Path = version_file_in_current_dir
        version: str = "1.0.0"
        version_with_whitespace: str = f"{version}  \n\n  "
        version_file.write_text(version_with_whitespace)
        resolved_version: str = VersionFileBased(version_file_name=version_file.name).resolve_version()
        assert resolved_version == version
