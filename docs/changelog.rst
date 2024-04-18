Changelog
=============

0.6.1
----------
* Improvement: remove django-appconf implicit dependency (`#84 <https://github.com/preply/dj_anonymizer/pull/84>`__)

0.6.0
----------
* Feature: adds possibility to truncate with cascade option (`#73 <https://github.com/preply/dj_anonymizer/pull/73>`__)

0.5.1
----------
* Bugfix: fix issue when model manager is overridden (`#71 <https://github.com/preply/dj_anonymizer/pull/71>`__)

0.5.0
----------
* Feature: add possibility to execute anonymizer only on the specified model (`#69 <https://github.com/preply/dj_anonymizer/pull/69>`__)
* Feature: raise exception if model registered, but database table does not exist (`#63 <https://github.com/preply/dj_anonymizer/pull/63>`__)
* Improvement: moved to GitHub Actions (`#64 <https://github.com/preply/dj_anonymizer/pull/64>`__)

0.4.0
----------
* Feature: possibility to truncate register_clean tables (`#41 <https://github.com/preply/dj_anonymizer/pull/41>`__)
* Feature: infer exclude_fields when property is not set (`#45 <https://github.com/preply/dj_anonymizer/pull/45>`__)
* Feature: --check-only mode (`#52 <https://github.com/preply/dj_anonymizer/pull/52>`__)
* Feature: Handle Windows paths in module import (`#54 <https://github.com/preply/dj_anonymizer/pull/54>`__)
* Improvement: remove support for EOL Django versions, django-bulk-update is no longer an optional dependency (`#55 <https://github.com/preply/dj_anonymizer/pull/55>`__)

Breaking:

* Improvement: removed `register_clean_with_rules` method which now covered via `register_clean` (`#39 <https://github.com/preply/dj_anonymizer/pull/39>`__)
* Improvement: rename `anonym_field` to `fields` for more convenience (`#34 <https://github.com/preply/dj_anonymizer/pull/34>`__)

0.3.1
----------
* Bugfix: for Django==2.2 dj_anonymizer raise ModuleNotFoundError (`#32 <https://github.com/preply/dj_anonymizer/pull/32>`__)

0.3.0
----------
* Feature: new field - password (`#25 <https://github.com/preply/dj_anonymizer/pull/25>`__)
* Feature: since Django 2.2 used native bulk_update. django-bulk-update as an optional dependency. (`#29 <https://github.com/preply/dj_anonymizer/pull/29>`__)

0.2.0
----------
This is the first release with changelog

* Improvement: add Travis CI with flake8 and isort onboard
* Improvement: fix broken .md description on PyPI
* Improvement: add .editorconfig
* Improvement: add tests
* Docs: docs released
* Python3: Python 3 support
