Changelog
=============
Unreleased
----------

* Feature: possibility to truncate register_clean tables (`#41 <https://github.com/preply/dj_anonymizer/pull/41>`__)
* Feature: infer exclude_fields when property is not set (`#45 <https://github.com/preply/dj_anonymizer/pull/45>`__)

Breaking:

* Improvement: removed `register_clean_with_rules` method which now covered via `register_clean` (`#39 <https://github.com/preply/dj_anonymizer/pull/39>`__)
* Improvement: rename `anonym_field` to `fields` for more convenience (`#34 <https://github.com/preply/dj_anonymizer/pull/34>`__)

0.3.1
----------
* Bugfix: for Django==2.2 dj_anonymizer raise ModuleNotFoundError (`#32 <https://github.com/preply/dj_anonymizer/pull/32>`__)

0.3.0
----------
* Feature: new field - password (`#25 <https://github.com/preply/dj_anonymizer/pull/25>`__)
* Feature: Since Django 2.2 used native bulk_update. django-bulk-update as optional dependency. (`#29 <https://github.com/preply/dj_anonymizer/pull/29>`__)

0.2.0
----------
This is first release with changelog

* Improvement: add travis CI with flake8 and isort onboard
* Improvement: fix broken .md description on PyPI
* Improvement: add .editorconfig
* Improvement: add tests
* Docs: docs released
* Python3: Python 3 support
