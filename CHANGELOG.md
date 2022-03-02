# Mindee Python API Helper Changelog

## v2.1.0 (2022-03-02)

### Changes

* :sparkles: update to Invoices API v3
* :recycle: refactor `Endpoint` classes and document building
* :arrow_up: Update PikePDF to 5.0.1
* :sparkles: add a basic logger

## v2.0.2 (2022-02-21)

### Fixes
* :bug: fix sending financial document via the CLI

### Changes
* :sparkles: allow getting OCR return in CLI
* :sparkles: Make sure all document information is printed

## v2.0.1 (2022-02-15)

### Fixes
* :bug: fix for invoice to string
* :bug: fix for counting empty PDF pages

### Changes
* :arrow_up: Update PikePDF to 4.5.0
* :arrow_up: Update Pillow to 9.0.1 (security fix)

## v2.0.0 (2022-02-14)

### New Features
* :sparkles: Allow using custom documents (API builder)

### :boom: Breaking Changes
* :recycle: `probability` renamed to `confidence` in the return fields to match
  API return
* :recycle: `Client` initialization reworked to be more extensible
* :recycle: Document loading and parsing reworked to separate arguments

### Changes
* :arrow_up: Upgrade pikepdf to 4.4.1
* :memo: Documentation migrated mainly to https://developers.mindee.com/docs

## v1.3.1 (2022-02-03)

### Fixes
* :bug: fix probabilities not loaded from API
  [#49](https://github.com/mindee/mindee-api-python/issues/49)

### Changes
* :sparkles: add CLI tool for testing

## v1.3.0 (2022-01-17)

### Fixes
* :bug: Fixed URLs not built properly on Windows OS
  [#33](https://github.com/mindee/mindee-api-python/issues/33)
* :bug: fixed API error when using base64
  [#45](https://github.com/mindee/mindee-api-python/issues/45)

### Changes
* :sparkles: Add user-agent header with SDK and Python versions
* :sparkles: Use pikepdf to replace pyMuPDF
* :construction_worker: Pass all code through Black
* :pushpin: use `pip-tools` and `setup.py` to pin all dependencies
* :page_facing_up: change to MIT license

## v1.2.3 (2021-12-22)

### Fix

* :arrow_up: upgrade pymupdf to 1.18.17

### Bug

* :bug: handle few PDF files considered blank
* :white_check_mark: re-initialize file cursor in test

## v1.2.2 (2021-10-11)

### Fix

*  :bug: Fixed [#15](https://github.com/mindee/mindee-api-python/issues/15)

### Chg

* :sparkles: Added pdf page number parameter for multi-pages pdfs
* :sparkles: Added a blank pages only PDF detection & error raising


## v1.2.1 (2021-09-23)

### Fix

* :bug: Forward uploaded file name for file verification rules
* :bug: Change token management for new header format

## v1.2.0 (2021-08-25)

### Chg

* :sparkles: Adapted SDK to the new Mindee API endpoint
* :zap: Single page object reconstruction is now server-side
* :heavy_minus_sign: Removed Numpy dependency
* :white_check_mark: Updated tests with new data

## v1.1.3 (2021-02-21)

### Fix

* :zap: FinancialDoc attributes have same type from invoice or receipt

## v1.1.2 (2021-02-19)

### Fix

* :bug: Fixed FinancialDoc invoice version and reconstruction

## v1.1.1 (2021-01-31)

### Chg

* Updated total tax reconstruction for invoice

## v1.1.0 (2020-12-02)

### Chg

* Updated invoice API endpoint to V2

## v1.0.2 (2020-12-01)

### Fix

* Fixed null tax rate issue

## v1.0.0 (2020-10-28)

### New

* ✨ First release
