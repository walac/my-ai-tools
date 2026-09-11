"""Behavioral tests for the kernel tutorial checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CHECKER = SKILL_DIR / "scripts" / "check-tutorial"
TREE = SKILL_DIR / "evals" / "files" / "mini-kernel"


class CheckTutorialTests(unittest.TestCase):
    def run_checker(
        self,
        tutorial: str,
        files: tuple[str, ...],
        *,
        expect_errors: bool = True,
        file_text: str = "line one\n",
    ) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relpath in files:
                target = root / relpath
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(file_text, encoding="utf-8")
            draft = root / "tutorial.md"
            draft.write_text(tutorial, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(draft), "--tree", str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
        expected = 1 if expect_errors else 0
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

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

    def test_allows_unlinked_later_mention_in_the_same_subsection(self) -> None:
        """Only the first symbol mention in a subsection carries an Elixir link."""
        tutorial = """## API {#api}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L11)
is invoked during boot through `fake_key_enable()`.
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

    def test_rejects_symbol_link_drift_across_subsections(self) -> None:
        """Re-linking a symbol elsewhere must retain its original source line."""
        tutorial = """## API {#api}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L11)
enables the key.

---
## Boot {#boot}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/init/main.c#L2)
is called during early boot.
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
        self.assertIn("fake_key_enable elixir link drifts", result.stdout)

    def test_allows_struct_tag_and_ordinary_symbol_with_the_same_spelling(self) -> None:
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

    def test_validates_elixir_links_in_headings(self) -> None:
        output = self.run_checker(
            """# Tutorial

## [kernel/fake_key.c](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c) {#overview}

### [kernel/missing.c](https://elixir.bootlin.com/linux/v6.15/source/kernel/missing.c#L1) {#missing}
""",
            ("kernel/fake_key.c",),
        )
        self.assertIn("elixir path not in tree: kernel/missing.c", output)
        self.assertIn("elixir links mix versions ['v6.15', 'v6.16']", output)

    def test_requires_links_for_extensionless_in_tree_paths(self) -> None:
        output = self.run_checker(
            """# Tutorial

## Overview {#overview}

See arch/x86/Kconfig for the configuration.
""",
            ("arch/x86/Kconfig",),
        )
        self.assertIn("in-tree path arch/x86/Kconfig is not an elixir link", output)

    def test_requires_links_for_sentence_final_paths(self) -> None:
        output = self.run_checker(
            """# Tutorial

## Overview {#overview}

See kernel/fake_key.c.
""",
            ("kernel/fake_key.c",),
        )
        self.assertIn("in-tree path kernel/fake_key.c is not an elixir link", output)

    def test_requires_each_path_occurrence_to_be_linked(self) -> None:
        output = self.run_checker(
            """# Tutorial

## Overview {#overview}

[kernel/fake_key.c](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1) and kernel/fake_key.c describe the mechanism.
""",
            ("kernel/fake_key.c",),
        )
        self.assertIn("in-tree path kernel/fake_key.c is not an elixir link", output)

    def test_rejects_second_elixir_link_for_symbol_in_subsection(self) -> None:
        # Two elixir links to the same ident under one ## must fail even when #L is valid.
        output = self.run_checker(
            """# Tutorial

## Overview {#overview}

[fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1)
later [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1)
""",
            ("kernel/fake_key.c",),
            file_text="void fake_key_enable(void)\n",
        )
        self.assertIn(
            "fake_key_enable already elixir-linked in this subsection (line 5 col 1)",
            output,
        )

    def test_same_line_duplicate_link_names_first_column(self) -> None:
        # Same-line duplicates should point at the first link's column, not re-emit #L mismatch.
        output = self.run_checker(
            """# Tutorial

## Overview {#overview}

[fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1) and [fake_key_enable()](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1)
""",
            ("kernel/fake_key.c",),
        )
        self.assertIn(
            "fake_key_enable already elixir-linked earlier on this line (col 1)",
            output,
        )
        self.assertEqual(output.count("does not contain 'fake_key_enable'"), 1)

    def test_golden_tutorial_passes(self) -> None:
        # The checked-in specimen must stay a clean success against the mini-kernel tree.
        golden = SKILL_DIR / "evals" / "files" / "golden-tutorial.md"
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(golden), "--tree", str(TREE)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)


if __name__ == "__main__":
    unittest.main()
