import subprocess
from unittest.mock import patch, Mock

from devbootstrap.bootstrap import discover_github


def test_discover_github_returns_urls():
    mock_result = Mock()
    mock_result.stdout = (
        "https://github.com/foo/repo1\n"
        "https://github.com/foo/repo2\n"
    )

    with patch("devbootstrap.bootstrap.subprocess.run", return_value=mock_result):
        result = discover_github("foo")

    assert result == [
        "https://github.com/foo/repo1",
        "https://github.com/foo/repo2",
    ]