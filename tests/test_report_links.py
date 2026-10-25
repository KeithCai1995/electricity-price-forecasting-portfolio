"""Link resolution needs no optional PDF-rendering dependencies."""
from pathlib import Path
import importlib.util
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("report_link_builder", ROOT / "scripts/build_report.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class TestReportLinks(unittest.TestCase):
    def test_current_report_internal_links_resolve_to_existing_repository_files(self):
        source = ROOT / "report/report_v110.md"
        checked = 0
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^\s)]+)\)", source.read_text(encoding="utf-8")):
            if urlsplit(target).scheme or urlsplit(target).netloc:
                continue
            resolved = BUILDER.pdf_link_target(target, source)
            prefix = BUILDER.REPOSITORY_URL + "/blob/main/"
            self.assertTrue(resolved.startswith(prefix))
            relative = unquote(urlsplit(resolved[len(prefix):]).path)
            self.assertTrue((ROOT / relative).is_file(), resolved)
            checked += 1
        self.assertGreater(checked, 0)

    def test_external_links_are_unchanged(self):
        for target in ("https://arxiv.org/abs/1905.03222", "https://example.org/?a=1&b=2"):
            self.assertEqual(BUILDER.pdf_link_target(target, ROOT / "report/report_v110.md"), target)

    def test_query_fragment_and_encoded_spaces_are_preserved(self):
        source = ROOT / "report/report_v110.md"
        prefix = BUILDER.REPOSITORY_URL + "/blob/main/"
        self.assertEqual(BUILDER.pdf_link_target("../README.md?plain=1#reproduce", source),
                         prefix + "README.md?plain=1#reproduce")
        self.assertEqual(BUILDER.pdf_link_target("../folder/a%20file.md", source),
                         prefix + "folder/a%20file.md")
        self.assertEqual(BUILDER.pdf_link_target("#results", source),
                         prefix + "report/report_v110.md#results")

    def test_links_outside_repository_are_rejected(self):
        with self.assertRaises(ValueError):
            BUILDER.pdf_link_target("../../outside.md", ROOT / "report/report_v110.md")


if __name__ == "__main__":
    unittest.main()
