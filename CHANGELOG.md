# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.3] - 2026-07-31

### Changed

- Replace ste100vocab dependency with biz-dfch-asdste100vocab>=0.8.0.

### Added

- CI: correct step indentation in `ci.yml` and `publish.yml`.

## [2.1.2] - 2026-07-28

### Added

- CI test for tool availability (pylint, ruff).
- Ruff format and check in build steps.
- Suppress Sonar false positive warnings (`python:S3358`, `githubactions:S8541`).

### Changed

- Bump version to 2.1.2; update vocab dependency to 0.7.1.

### Fixed

- Correct ruff error DTZ005.
- SonarQube warning in test code.

## [2.1.1] - 2026-07-28

### Changed

- Remove unused archive files from documentation.
- Bump version to 2.1.1.

### Fixed

- Correct `git tag` example in documentation.

## [2.1.0] - 2026-07-27

### Added

- Readline shortcuts in interactive input loop.
- Release instructions; update copyright year to 2026.

### Changed

- CI: align and harden CI/CD workflows (uv sync/run configuration).
- Replace black and Flake8 with ruff across the codebase.
- Align pylint and ruff configuration; apply ruff formatting.

### Fixed

- PyInstaller version check runs after dependency installation.
- Publish workflow: add `--frozen --no-build` flags to uv commands.

## [2.0.5] - 2026-07-23

### Changed

- Update copyright year; bump vocab dependency to 0.7.0.

### Fixed

- Dictionary command: render all STE/non-STE examples for rejected words.
- Remove unused imports in i18n.

### Refactored

- Suppress Sonar S3776 false positives on complex methods.
- Reduce cognitive complexity in `WordCategoryCommand`, `WordFilter`, and `RuleRenderer`.
- Remove sentence analysis feature.

## [2.0.4] - 2026-07-21

### Added

- Dictionary command and ASD-STE100 rules processing.

### Removed

- Parse command and unused parser files.

## [2.0.0–2.0.3] - Pre-Publication (2026)

CI/CD pipeline: publish workflow, GitHub Actions setup, PyInstaller spec.
Initial release to PyPI with binary assets bundled for distributions.

## [1.10.0] - 2025

### Changed

- CLI default command refined; spelling corrections across commands.
- Dictionary files support extended (COLORS, People categories).
- Default command text processing updated.

## [1.9.0] - 2025

### Added

- Full-text query to rule text for broader matching.

### Changed

- Version bumped to 1.9.0.

## [1.8.0] - 2024

### Added

- Word categories command with categorization of dictionary words.
- Description with inline examples for category help output.
- `SentenceInfo` data structure.

## [1.7.1] - 2024

### Fixed

- Dictionary processing corrections.
- Improved logging; cleanup across commands.

## [1.7.0] - 2024

### Added

- Word count function (WIP).
- Custom words and colouring support.
- CONTRIBUTING guide; SECURITY policy; issue templates.

### Changed

- Rules processing updated; refactoring of core logic.
- Formatting improvements.

## [1.6.0] - 2024

### Added

- Filter command for narrowing dictionary results.

## [1.5.0] - 2023–2024

### Added

- Dictionary command with save/exit commands.
- Random word selection feature.

### Changed

- Main prompt changed from argument to command interface.
- Extensive refactoring of core modules; Black formatting applied.
- Removed unused files.

## [1.4.2] - 2023

### Fixed

- Suppress SonarCube warnings throughout codebase.
- Remove SonarCloud badges and related noise.

### Added

- Random word selection app features.

## [1.4.1] - 2023

### Fixed

- Spelling errors, formatting, page numbers, and missing STE examples.
- Unicode character for ohm symbol; corrected links in documentation.
- Minor corrections across categories.

### Added

- CODE_OF_CONDUCT.md; funding.yml.

## [1.4.0-beta1] - 2023

### Added

- Rule renderer engine (`RuleRenderer`).
- Technical words parser and dictionary file parser.
- Exit command and save command infrastructure.
- CI workflow (`ci.yml`); pylint configuration; Dependabot support.

## [1.3.1] - 2023

### Fixed

- Missing dacite library in compiled ARM build.

### Changed

- Minor logging adjustments; `save_command` refinements.

## [1.3.0] - 2022–2023

### Added

- Source and category information for dictionary words.
- Comprehensive rule processing (rules 5.1–5.5).
- JSON loading infrastructure; rules engine implementation.

### Fixed

- Word mappings: DRAIN/DRAIN, NOW/AT THIS TIME, SWING alternatives.
- Formatting corrections across multiple entries; evaluation fixes.

### Changed

- Major refactoring of core processing logic and rule engine.

## [1.2.0] - 2022

### Added

- Multiple alternative examples for dictionary words.
- Verbose help output.

### Fixed

- Log level detection.
- CLI arguments for input/output; removed hard-coded dictionary file.

## [1.1.0] - 2022

Standards extraction and additional CLI argument support.

## [1.0.4-beta] - 2021–2022

### Added

- CLI support via argparse; ASD-STE100 dictionary command.
- Application prompt user loop.

### Fixed

- Word entries: "extract", "at least".

## [1.0.1-beta] - 2021

### Changed

- Removed previous unused parsing routing.
- Updated codebase to work with `.prj` project files.

## [1.0.0-beta] - Initial Release

Initial prototype of the ASD-STE100 Lookup tool.

[Unreleased]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.1.2...HEAD
[2.1.2]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.0.5...v2.1.0
[2.0.5]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v2.0.3...v2.0.4
[2.0.0–2.0.3]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.10.0...v2.0.0
[1.10.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.9.0...v1.10.0
[1.9.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.7.1...v1.8.0
[1.7.1]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.4.2...v1.5.0
[1.4.2]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.4.0-beta1...v1.4.1
[1.4.0-beta1]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.3.1...v1.4.0-beta1
[1.3.1]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.0.4-beta...v1.1.0
[1.0.4-beta]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.0.1-beta...v1.0.4-beta
[1.0.1-beta]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/compare/v1.0.0-beta...v1.0.1-beta
[1.0.0-beta]: https://github.com/dfch/biz.dfch.AsdSte100Lookup/tree/v1.0.0-beta
