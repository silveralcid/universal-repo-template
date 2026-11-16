# Sharing a source package

## Scope and limits

This procedure minimizes direct identifiers and archive metadata. It does not guarantee anonymity, erase public history, or prevent source-code comparison. Do not describe a passing scan as proof that a package cannot be attributed.

Review the intended audience before sharing. Source may be linked to an earlier copy through matching code, prose, filenames, file hashes, or directory structure. Repository ownership, commit author and committer fields, pull requests, release assets, forks, logs, and the message used to deliver an archive are separate attribution surfaces.

## Build a reviewed archive

Use a clean source snapshot. Review every file listed in `.repo/template-manifest.json`, then verify that the manifest hashes match that snapshot. Do not add private project records simply to make a hash check pass. Preserve third-party attribution and security pins.

```sh
python tools/repo.py check --tests
python tools/repo.py docs budget --strict
python tools/export_source.py --output ../project-starter.zip
```

The exporter reads only the manifest-listed UTF-8 source files and the manifest itself. It refuses unsafe paths, symlinks, common private/local paths, hash mismatches, oversized files, common credential patterns, and non-example email addresses. Unlisted local files are not packaged. These checks are deliberately limited and do not replace a dedicated secret scanner or human review.

The ZIP has a generic root directory, a fixed baseline timestamp, normalized file attributes, no entry comments, no extra fields, and no archive comment. It contains no Git directory, commit history, remotes, or local verification receipts. The output is created exclusively: an existing file is never overwritten.

## Project-specific checks

Keep a private list of sensitive names, usernames, domains, customer identifiers, source commit hashes, and project titles outside the repository. Put one literal term on each line. Do not publish that list, even in a test fixture, audit report, or commit message.

```sh
python tools/export_source.py --denylist-file ../private-terms.txt --output ../project-starter.zip
```

Terms are matched case-insensitively against paths and text. Findings report categories and relative paths without printing matched values. The denylist must be outside the source root and is never packaged. Passing only proves that the configured checks found no matches.

## Continuous source-independence checks

The repository health workflow runs `python3 tools/export_source.py --check-tracked --repository "$GITHUB_REPOSITORY"`. This checks the whole reviewed manifest, rejects unmanifested Git-tracked files, and detects links to *different repositories owned by the same GitHub account* across GitHub HTTPS, SSH, raw-content and API URLs. It does not require embedding any personal project names in the public repository.

These generic checks cannot recognize every employer, customer, code name or distinctive phrase. Before publishing a template for reuse, supply an external, private `--denylist-file` containing sensitive names and identifiers. Keep that list and its scan output outside the source tree; run the check after the final source edit. A clean current archive does not sanitize prior public commits, pull-request revisions, GitHub caches, forks or external copies. Treat cleanup of historical public objects as a separately planned operation rather than a routine force push.

## Public hosting

Do not use a personally identifying account for an anonymity-sensitive publication. Changing visible files does not remove older versions, author metadata, pull-request references, archived releases, or other people's copies. History rewriting is a separate, coordinated operation and may invalidate signatures, break open pull requests, or discard concurrent work.

A fresh repository without inherited history reduces some metadata links but cannot hide the origin of recognizable source. Preserve required notices. Do not rely on cosmetic renaming, generic commit authors, private visibility, or rewritten prose as an anonymity guarantee.

Keep detailed private audit findings separate from the distributable. Never place the identifiers that were removed back into the public repository as examples or remediation notes.
