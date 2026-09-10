"""Behavioral tests for the kernel tutorial checker."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CHECKER = SKILL_DIR / "scripts" / "check-tutorial"
TREE = SKILL_DIR / "evals" / "files" / "mini-kernel"


class CheckTutorialTests(unittest.TestCase):
    def test_allows_file_level_elixir_link_without_line_anchor(self) -> None:
        """A documentation-file reference need not pretend to name a symbol."""
        tutorial = """## Further reading {#further-reading}

Read [the fake-key documentation](https://elixir.bootlin.com/linux/v6.16/source/Documentation/core-api/fake_key.rst).
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(TREE)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_allows_identifier_named_file_link_without_line_anchor(self) -> None:
        """A whole-file link may use the file's identifier-shaped basename."""
        tutorial = """## Further reading {#further-reading}

Read the [Makefile](https://elixir.bootlin.com/linux/v6.16/source/Makefile).
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(TREE)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_still_rejects_symbol_link_without_line_anchor(self) -> None:
        """The relaxation must not swallow the case it was meant to keep failing."""
        tutorial = """## Overview {#overview}

The [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c) function turns the key on.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(TREE)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbol elixir link has no #L<number>", result.stdout)

    def test_still_rejects_struct_link_without_line_anchor(self) -> None:
        """A `struct foo` label is a symbol reference even though it has a space."""
        tutorial = """## Data structures {#data-structures}

The only type is [`struct fake_key`](https://elixir.bootlin.com/linux/v6.16/source/include/linux/fake_key.h).
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(TREE)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbol elixir link has no #L<number>", result.stdout)

    def test_keeps_type_and_ordinary_symbols_in_separate_consistency_namespaces(self) -> None:
        """A struct tag and an ordinary C symbol may share a spelling."""
        tutorial = """## API {#api}

The [`struct foo`](https://elixir.bootlin.com/linux/v6.16/source/example.c#L1)
type is passed to [`foo()`](https://elixir.bootlin.com/linux/v6.16/source/example.c#L4).
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tree = Path(tmpdir) / "tree"
            tree.mkdir()
            (tree / "example.c").write_text(
                "struct foo { int value; };\n\nvoid unused(void);\nvoid foo(void) {}\n",
                encoding="utf-8",
            )
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(tree)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_file_level_link_to_a_path_outside_the_tree(self) -> None:
        """Relaxing anchors must not skip the existing path check."""
        tutorial = """## Further reading {#further-reading}

Read [a missing document](https://elixir.bootlin.com/linux/v6.16/source/Documentation/missing.rst).
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tutorial.md"
            path.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [str(CHECKER), str(path), "--tree", str(TREE)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("elixir path not in tree", result.stdout)


if __name__ == "__main__":
    unittest.main()
