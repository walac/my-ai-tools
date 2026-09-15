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
            command = [sys.executable, str(CHECKER), str(draft), "--tree", str(root)]
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
            )
        expected = 1 if expect_errors else 0
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_allows_file_level_elixir_link_without_line_anchor(self) -> None:
        """A documentation-file reference need not pretend to name a symbol."""
        tutorial = """# Tutorial

## Further reading {#further-reading}

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
        tutorial = """# Tutorial

## Further reading {#further-reading}

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
        tutorial = """# Tutorial

## Overview {#overview}

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
        """An unlinked later mention remains valid regardless of link density."""
        tutorial = """# Tutorial

## API {#api}

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

    def test_allows_same_symbol_spelling_in_distinct_definitions(self) -> None:
        """Link choices must not assume an identifier has one global definition."""
        tutorial = """# Tutorial

## API {#api}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1)
is one definition.

---
## Boot {#boot}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/init/main.c#L1)
is another definition with the same spelling.
"""
        output = self.run_checker(
            tutorial,
            ("kernel/fake_key.c", "init/main.c"),
            expect_errors=False,
            file_text="void fake_key_enable(void) {}\n",
        )
        self.assertIn("0 error(s)", output)

    def test_allows_same_symbol_spelling_for_distinct_definitions_in_subsection(self) -> None:
        """Duplicate checks distinguish definitions, not only their spelling."""
        tutorial = """# Tutorial

## Architecture comparison {#architecture-comparison}

[`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/kernel/fake_key.c#L1)
is the generic definition. [`fake_key_enable()`](https://elixir.bootlin.com/linux/v6.16/source/init/main.c#L1)
is the architecture-specific definition.
"""
        output = self.run_checker(
            tutorial,
            ("kernel/fake_key.c", "init/main.c"),
            expect_errors=False,
            file_text="void fake_key_enable(void) {}\n",
        )
        self.assertIn("0 error(s)", output)

    def test_allows_struct_tag_and_ordinary_symbol_with_the_same_spelling(self) -> None:
        """A struct tag and an ordinary C symbol may share a spelling."""
        tutorial = """# Tutorial

## API {#api}

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

    def test_rejects_repeated_elixir_links_for_a_symbol(self) -> None:
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

    def test_requires_kernel_tutorial_section_structure(self) -> None:
        output = self.run_checker(
            """# Fake keys

An explanation organized around the requested call path.

## 1 The call path

The caller reaches the update path after incrementing the counter.

### Why the order matters

The update observes the completed transition.

## Where the state lives

The state is shared by all callers.
""",
            (),
        )
        self.assertIn("heading has a section number", output)
        self.assertIn("heading missing {#slug}", output)
        self.assertIn("is not preceded by ---", output)

    def test_warns_about_possessive_prose(self) -> None:
        output = self.run_checker(
            """# Fake keys

The mechanism's counter is shared between callers.

## State {#state}

The key's state changes on the boundary transition.
""",
            (),
            expect_errors=False,
        )
        self.assertIn("2 warning(s)", output)
        self.assertIn('possessive "mechanism\'s"', output)
        self.assertIn('possessive "key\'s"', output)

    def test_requires_document_title_on_first_line(self) -> None:
        output = self.run_checker(
            """An explanation organized around the requested call path.

## Where the state lives {#where-the-state-lives}

The state is shared by all callers.
""",
            (),
        )
        self.assertIn("first line must be a document-title H1", output)

    def test_rejects_slug_on_document_title(self) -> None:
        output = self.run_checker(
            """# Fake keys {#fake-keys}

## State {#state}

The state is shared by all callers.
""",
            (),
        )
        self.assertIn("document-title H1 must not have a {#slug}", output)

    def test_rejects_unfilled_skeleton_markers(self) -> None:
        output = self.run_checker(
            """# TITLE

## Replace-this-heading {#replace-this-heading}

Tutorial text.
""",
            (),
        )
        self.assertIn("leftover skeleton title", output)
        self.assertIn("leftover skeleton heading", output)

    def test_topic_shaped_headings_without_canned_toc_pass(self) -> None:
        """The checker must not require Overview / Data structures / Life of a …"""
        output = self.run_checker(
            """# Fake keys

A counted switch.

## Enabling a key {#enabling-a-key}

Framing for the enable path.

---

## Poll budget {#poll-budget}

Framing for a topic-shaped middle section.

---

## Further reading in-tree {#further-reading-in-tree}

Next files.
""",
            (),
            expect_errors=False,
        )
        self.assertIn("0 error(s)", output)

    def test_single_h2_without_further_reading_passes(self) -> None:
        """A usage-only walk may be one H2; a closer is not a mechanical rule."""
        output = self.run_checker(
            """# Fake keys

A counted switch.

## Enabling a key {#enabling-a-key}

Framing for a usage-only walk.
""",
            (),
            expect_errors=False,
        )
        self.assertIn("0 error(s)", output)

    def test_canned_toc_titles_are_allowed(self) -> None:
        """Overview-style titles are not banned; they are also not required."""
        output = self.run_checker(
            """# Fake keys

A counted switch.

## Overview {#overview}

Framing.

---

## Data structures {#data-structures}

Framing.
""",
            (),
            expect_errors=False,
        )
        self.assertIn("0 error(s)", output)

    def test_broken_tutorial_fails(self) -> None:
        broken = SKILL_DIR / "evals" / "files" / "broken-tutorial.md"
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(broken), "--tree", str(TREE)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("heading has a section number", result.stdout)
        self.assertIn("heading missing {#slug}", result.stdout)

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
