"""Regression coverage for reviewed source export and metadata minimization."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import export_source as package


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        (self.root / '.repo').mkdir()
        self.write('README.md', b'# Example\n')
        self.manifest({'README.md': b'# Example\n'})

    def write(self, path, data):
        output = self.root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)

    def manifest(self, entries):
        (self.root / package.MANIFEST).write_text(json.dumps({
            'algorithm': 'sha256',
            'files': {name: hashlib.sha256(data).hexdigest() for name, data in entries.items()}
        }))

    def test_only_reviewed_files_are_exported(self):
        self.write('unlisted.txt', b'not reviewed')
        self.assertEqual(set(package.load_payload(self.root)), {'README.md', package.MANIFEST})

    def test_changed_file_fails_closed(self):
        self.write('README.md', b'changed')
        with self.assertRaises(ValueError):
            package.load_payload(self.root)

    def test_missing_file_fails_closed(self):
        (self.root / 'README.md').unlink()
        with self.assertRaises(ValueError):
            package.load_payload(self.root)

    def test_private_paths_and_traversal_are_rejected(self):
        for path in ('../outside', '/absolute', '.git/config', '.env', 'a/../b',
                     'a\\b', 'a//b', './README.md', '.repo-local/receipt.json', 'secret.pem'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                package.checked_path(self.root.resolve(), path)

    def test_symlink_is_rejected(self):
        link = self.root / 'alias.md'
        try:
            link.symlink_to(self.root / 'README.md')
        except (NotImplementedError, OSError):
            self.skipTest('Symlinks unavailable')
        with self.assertRaises(ValueError):
            package.checked_path(self.root.resolve(), 'alias.md')

    def test_metadata_and_content_are_verified(self):
        payload = package.load_payload(self.root)
        output = Path(self.temp.name) / 'source.zip'
        package.export(payload, output)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.comment, b'')
            self.assertIsNone(archive.testzip())
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, package.STAMP)
                self.assertEqual(entry.comment, b'')
                self.assertEqual(entry.extra, b'')
                self.assertEqual(entry.create_system, 0)
                self.assertEqual(archive.read(entry), payload[entry.filename.split('/', 1)[1]])

    def test_output_is_repeatable(self):
        payload = package.load_payload(self.root)
        first, second = (Path(self.temp.name) / name for name in ('one.zip', 'two.zip'))
        package.export(payload, first)
        package.export(payload, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_existing_output_is_not_overwritten(self):
        output = Path(self.temp.name) / 'existing.zip'
        output.write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            package.export(package.load_payload(self.root), output)
        self.assertEqual(output.read_bytes(), b'preserve')

    def test_private_terms_are_case_insensitive_and_not_printed(self):
        value = 'FixtureIdentity'
        result = package.findings({'a.txt': value.upper().encode()}, (value,))
        self.assertEqual(result, ['a.txt: private denylist match'])
        self.assertNotIn(value, '\n'.join(result))

    def test_private_terms_in_filenames_are_detected(self):
        self.assertTrue(package.findings({'fixture-project.txt': b'ok'}, ('fixture-project',)))

    def test_only_example_email_domains_are_allowed(self):
        self.assertFalse(package.findings({'a.txt': b'template@example.invalid'}))
        address = ('fixture' + '@' + 'mail.test').encode()
        self.assertTrue(package.findings({'a.txt': address}))

    def test_token_patterns_are_detected_without_echo(self):
        token = 'ghp_' + 'A' * 30
        result = package.findings({'a.txt': token.encode()})
        self.assertTrue(result)
        self.assertNotIn(token, '\n'.join(result))

    def test_binary_data_is_rejected(self):
        data = b'a\0b'
        self.write('README.md', data)
        self.manifest({'README.md': data})
        with self.assertRaises(ValueError):
            package.load_payload(self.root)

    def test_case_collisions_are_rejected(self):
        self.write('readme.md', b'different')
        self.manifest({'README.md': b'# Example\n', 'readme.md': b'different'})
        with self.assertRaises(ValueError):
            package.load_payload(self.root)

    def test_non_utf8_is_rejected(self):
        self.write('README.md', b'\xff')
        self.manifest({'README.md': b'\xff'})
        with self.assertRaises(UnicodeError):
            package.load_payload(self.root)


if __name__ == '__main__':
    unittest.main()
