# Mindee Python API Library Changelog

## v3.11.0 - 2023-07-03
### Changes
* :sparkles: add basic support for line items
* :sparkles: add support for FR bank account details v2


## v3.10.0 - 2023-06-26
### Changes
* :coffin: remove support for Shipping Container
* :sparkles: add OpenAPI GET request
* :sparkles: add OCR output in CLI
* :sparkles: add support for material certificate v1

### Fixes
* :bug: fix potential problem where the words can be re-arranged by the user when calculating lines.


## v3.9.1 - 2023-06-07
### Changes
* :memo: add documentation for OCR extraction


## v3.9.0 - 2023-06-06
### Changes
* :sparkles: add support for financial documents v1.1
* :sparkles: add support for handling OCR return
* :recycle: update printing of receipt, invoice, financial doc


## v3.8.2 - 2023-05-23
### Changes
* :recycle: add a specific class for classifications, which are never None

### Fixes
* :bug: fix for tax base amount


## v3.8.1 - 2023-05-11
### Fixes
* :bug: fix naming of job ID property


## v3.8.0 - 2023-05-10
### Changes
* :sparkles: add support for Invoice Splitter V1
* :sparkles: add support for asynchronous requests


## v3.7.1 - 2023-04-20
### Fixes
* :bug: fix EU imports, use short imports in tests


## v3.7.0 - 2023-04-18
### Changes
* :sparkles: add support for receipt v5
* :white_check_mark: use code samples for integration testing


## v3.6.0 - 2023-03-10
### Changes
* :sparkles: add an URL input source
* :memo: add proof of address documentation
### Fixes
* :bug: fix file extension for sample code inclusion


## v3.5.0 - 2023-02-17
### Changes
* :safety_vest: make sure CI is run on various OSes
* :arrow_up: general update to all dependencies
* :sparkles: add support for FR carte vitale v1
* :sparkles: add support for FR ID card v1
* :sparkles: add support for shipping container v1
* :sparkles: add EU license plate v1
* :memo: add sample code for all supported APIs

### Fixes
* :bug: fix for null classification field on custom APIs


## v3.4.0 - 2023-02-01
### Changes
* :sparkles: add support for: financial document v1
* :sparkles: add support for: proof of address v1

### Deprecations
The `FinancialV1` class is now *deprecated*.

It's still usable with no code modifications but will be **removed** in a future release.

All users are encouraged to move to `FinancialDocumentV1` which has much better performance.
Also field names in `FinancialDocumentV1` now match those of `Invoice` and `Receipt`.


## v3.3.0 - 2023-01-27
### Changes
* sparkles: Add French carte grise v1 support


## v3.2.1 - 2023-01-18
### Changes
* :arrow_up: Update pikepdf
* :sparkles: Add support for Python 3.11

### Fixes
* :bug: Fix misleading docstrings


## v3.2.0 - 2023-01-06
### Changes
* :sparkles: add version option in CLI
* :recycle: harmonize printing of float values
* :sparkles: add support for Invoice 4.1
* :sparkles: add support for Receipt v4.1
* :memo: reorganize docs a bit
* :arrow_up: update dependencies


## v3.1.1 - 2022-12-02
### Fixes
* :bug: fix for invoice v4 URL


## v3.1.0 - 2022-12-01
### Changes
* :sparkles: allow setting base URL from env
* :sparkles: add some helper functions for BBox
* :sparkles: Add orientation info on all pages
* :sparkles: add Cropper support
* :sparkles: allow setting timeout value from env
* :sparkles: Add Invoice V4 (clearer field names, line items) (#107)

### Fixes
* :bug: page_n should always be set when available (#106)


## v3.0.0 - 2022-11-07
### ¡Breaking Changes!
* :sparkles: New PDF cut/merge system, allowing specifying exactly which pages to use.
* :recycle: PDF documents are no longer cut by default, use the `page_options` parameter in the `parse` method.
* :sparkles: Document (endpoints) are now versioned, providing better backward-compatible support.
* :sparkles: Pass the document class instead of a string to specify how to `parse` input sources.
* :recycle: Some methods and parameters renamed for better clarity.
* :sparkles: Results from Custom documents are now deserialized into objects, rather than `dict`.

### Changes
* :sparkles: Add support for expense receipts V4.
* :recycle: minor improvements to geometry functions.

### Fixes
* :bug: Make sure the user is specified when calling custom docs on CLI
* :bug: Add default timeout of 120 seconds for endpoints.


## v2.6.0 - 2022-10-10
### Fixes
* :bug: don't print "None" when filename is empty

### Changes
* :wastebasket: deprecate setting singular and plural names for docs (#98)
* :sparkles: add x-axis geometry functions (#99)
* :sparkles: add getting bounding box for multiple polygons (#100)
* :sparkles: add support for classifications in custom docs
* :sparkles: allow setting only the `MINDEE_API_KEY` environment variable
* :arrow_up: update pikepdf


## v2.5.1 - 2022-08-30
### Fixes
* :bug: never use mutable defaults in class definitions (#96)


## v2.5.0 - 2022-08-11
### Changes
* :lipstick: improve string output of documents
* :arrow_up: general dependencies upgrade (#92)
* :sparkles: add functions for working with centroids (#93)
* :sparkles: Add bank checks documents (beta, US only) (#94)


## v2.4.0 - 2022-06-20
### Fixes
* :bug: :memo: custom docs names refer to the API, not the type.
* :bug: words should be separated when printing custom documents
* :bug: empty date should return passport not in validity

### Changes
* :sparkles: Add TIFF and HEIC support
* :sparkles: Add real bounding boxes
* :memo: publish documentation to pages


## v2.3.0 - 2022-05-23
### Fixes
* :bug: make sure the 'Token' keyword is sent in the auth headers

### Changes
* :sparkles: now possible to read file contents at any time
* :hammer: run mypy in pre-commit
* :arrow_up: upgrade pikepdf
* :recycle: minor cleanup / refactor
* :memo: Add basic automated class documentation


## v2.2.0 - 2022-03-24
### Fixes
* :bug: :boom: fix for customer_company_registration being a list of values

### Changes
* :sparkles: allow specifying file closing behavior
* :arrow_up: loosen setup.py requirements; update pinned dependencies
* :white_check_mark: better testing of PDF pages


## v2.1.1 - 2022-03-15
### Fixes
* :bug: fix for locale constructor
* :bug: fix custom document in CLI
* :label: declare type info to mypy
* :bug: fix for dumping JSON in CLI

### Changes
* :label: set stricter pylint and mypy settings
* :technologist: add pre-commit to ensure proper code formatting
* :art: fixes to import order (isort) and documentation (pydocstyle)


## v2.1.0 - 2022-03-02
### Changes
* :sparkles: update to Invoices API v3
* :recycle: refactor `Endpoint` classes and document building
* :arrow_up: Update PikePDF to 5.0.1
* :sparkles: add a basic logger


## v2.0.2 - 2022-02-21
### Fixes
* :bug: fix sending financial document via the CLI

### Changes
* :sparkles: allow getting OCR return in CLI
* :sparkles: Make sure all document information is printed


## v2.0.1 - 2022-02-15
### Fixes
* :bug: fix for invoice to string
* :bug: fix for counting empty PDF pages

### Changes
* :arrow_up: Update PikePDF to 4.5.0
* :arrow_up: Update Pillow to 9.0.1 (security fix)


## v2.0.0 - 2022-02-14
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


## v1.3.1 - 2022-02-03
### Fixes
* :bug: fix probabilities not loaded from API
  [#49](https://github.com/mindee/mindee-api-python/issues/49)

### Changes
* :sparkles: add CLI tool for testing


## v1.3.0 - 2022-01-17
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


## v1.2.3 - 2021-12-22
### Fixes
* :arrow_up: upgrade pymupdf to 1.18.17
* :bug: handle few PDF files considered blank
* :white_check_mark: re-initialize file cursor in test


## v1.2.2 - 2021-10-11
### Fixes
*  :bug: Fixed [#15](https://github.com/mindee/mindee-api-python/issues/15)

### Changes
* :sparkles: Added pdf page number parameter for multi-pages pdfs
* :sparkles: Added a blank pages only PDF detection & error raising


## v1.2.1 - 2021-09-23
### Fixes
* :bug: Forward uploaded file name for file verification rules
* :bug: Change token management for new header format


## v1.2.0 - 2021-08-25
### Changes
* :sparkles: Adapted SDK to the new Mindee API endpoint
* :zap: Single page object reconstruction is now server-side
* :heavy_minus_sign: Removed Numpy dependency
* :white_check_mark: Updated tests with new data


## v1.1.3 - 2021-02-21
### Fixes
* :zap: FinancialDoc attributes have same type from invoice or receipt


## v1.1.2 - 2021-02-19
### Fix
* :bug: Fixed FinancialDoc invoice version and reconstruction


## v1.1.1 - 2021-01-31
### Changes
* Updated total tax reconstruction for invoice


## v1.1.0 - 2020-12-02
### Changes
* Updated invoice API endpoint to V2


## v1.0.2 - 2020-12-01
### Fix
* Fixed null tax rate issue


## v1.0.0 - 2020-10-28
* :tada: First release!
