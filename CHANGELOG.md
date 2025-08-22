# Mindee Python Client Library Changelog

## v4.27.1 - 2025-08-22
### Changes
* :recycle: use direct import of input classes
* :bug: fix broken location & confidence data for V2 fields
* :recycle:  make importing v2 classes easier


## v4.27.0 - 2025-07-30
### Changes
* :sparkles: add support for page count, mimetype + fixes
### Fixes
* :bug: fix jobs not deserializing webhook information into their proper class
* :bug: fix typo in `InferenceFile` class: `alais` => `alias`


## v4.26.0 - 2025-07-29
### Changes
* :sparkles: add support for URL inputs for V2


## v4.25.0 - 2025-07-18
### Changes
* :sparkles: add generic response loader


## v4.24.0 - 2025-07-17
### Changes
* :sparkles: Add support for mindee API V2 client & features
* :wrench: Tweak CI & testing
* :recycle: Uniformize variable naming across files
* :boom: remove support for Python 3.7


## v4.24.0-rc2 - 2025-07-09
### Changes
* :sparkles: merge enqueue parameters into a single object
* :sparkles: add dot access to object fields
### Fixes
* :recycle: remove deprecated files
* :art: touch up string representation for most objects.


## v4.24.0-rc1 - 2025-07-07
### Changes
* :sparkles: add support for mindee API V2 client & features
* :recycle: remove support for python 3.7
* :wrench: tweak CI & testing
* :recycle: uniformize variable naming across files


## v4.23.0 - 2025-06-03
### Changes
* :sparkles: add support for address fields
* :sparkles: add support for Financial Document V1.12
* :sparkles: add support for Invoices V4.10
* :sparkles: add support for US Healthcare Cards V1.2


## v4.22.0 - 2025-04-29
### Changes
* :sparkles: add support for workflow polling


## v4.21.1 - 2025-04-28
### Fixes
* :bug: fix for Python 3.10 and lower: server uses 'Z' in date string


## v4.21.0 - 2025-04-16
### Changes
* :sparkles: add support for RAG parameter in workflow executions


## v4.20.0 - 2025-04-08
### Changes
* :sparkles: add support for Financial Document V1.12
* :sparkles: add support for Invoices V4.10
* :sparkles: add support for US Healthcare Cards V1.2


## v4.19.1 - 2025-03-27
### Fixes
* :bug: fix for null objects in extras


## v4.19.0 - 2025-03-27
### Changes
* :sparkles: update structure for InvoiceSplitterV1
* :sparkles: update FR EnegryBillV1 to V1.2
* :sparkles: update US HealthcareCardV1 to V1.1
* :coffin: remove support for EU Driver License
* :coffin: remove support for PetrolReceiptV1
* :coffin: remove support for ReceiptV4
* :coffin: remove support for Proof of Address
* :coffin: remove support for US Driver License
* :coffin: remove support for US W9V1
### Fixes
* :bug: fix polling waiting for a full timeout in case of parsing failure
* :recycle: add missing imports for some products
* :arrow_down: downgrade pypdfium dependency due to very rare errors in local character extraction


## v4.18.0 - 2025-02-21
### Changes
* :sparkles: add support for image and pdf compression
* :recycle: increase async retry timers


## v4.17.0 - 2024-12-13
### Changes
* :sparkles: add support for us mail v3
* :art: linting fixes


## v4.16.0 - 2024-12-13
### Changes
* :sparkles: allow local downloading of remote sources
* :coffin: remove support for (FR) Carte Vitale V1 in favor of French Health Card V1


## v4.15.1 - 2024-11-28
### Changes
* :arrow_up: update pylint


## v4.15.0 - 2024-11-28
### Changes
* :sparkles: add support for workflows
* :sparkles: add support for French Health Card V1
* :sparkles: add support for Driver License V1
* :sparkles: add support for Payslip FR V3


## v4.14.2 - 2024-11-26
### Fixes
* :bug: fix circular imports error on install


## v4.14.1 - 2024-11-22
### Changes
* :coffin: remove support for international ID V1
* :recycle: update import syntax
* :arrow_up: loosen dependency pinning on requests

### Fixes
* :bug: fix potential circular import issues


## v4.14.0 - 2024-11-14
### Changes
* :sparkles: add support for business cards V1
* :sparkles: add support for delivery note V1.1
* :sparkles: add support for indian passport V1
* :sparkles: add support for resume V1.1
### Fixes
* :recycle: adjust default values for async delays
* :arrow_up: fully migrate project to pyproject.toml


## v4.13.0 - 2024-10-11
### Changes
* :sparkles: add support for Financial Document v1.10
* :sparkles: add support for Invoice v4.8


## v4.12.0 - 2024-09-18
### Changes
* :sparkles: add support for BillOfLadingV1
* :sparkles: add support for (US) UsMailV2
* :sparkles: add support for (FR) EnergyBillV1
* :sparkles: add support for (FR) PayslipV1
* :sparkles: add support for NutritionFactsLabelV1

### Fixes
* :bug: fixed a bug that prevented longer decimals from appearing in the string representation of some objects
* :bug: fixed a bug that caused non-table elements to unexpectedly appear truncated when printed to the console
* :bug: fix full text ocr extra not properly parsing
* :memo: fix a few documentation errors & typos
* :wrench: updated CI dependencies


## v4.11.0 - 2024-09-04
### Changes
* :sparkles: add support for full text OCR extra
* :sparkles: add support for invoice splitter auto-extraction
### Fixes
* :memo: add sample code example for image splitter auto-extraction
* :recycle: refactor `image_extraction` and change name to `extraction`
* :memo: update documentation
* :recycle: fix many typos in product internals
* :recycle: add a few missing `__init__.py` files


## v4.10.0 - 2024-07-24
### Changes
* :sparkles: add support for Healthcare Card V1
* :sparkles: add support for Invoice V4.7
* :sparkles: add support for Financial Document V1.9
* :sparkles: add support for BooleanField
* :recycle: update company registration display format
* :recycle: switch default image save format to PNG for image extractor

### Fixes
* :bug: fix invalid display when trying to cast null amount fields to string


## v4.9.0 - 2024-06-17
### Changes
* :sparkles: add support for complete multi-receipt extraction (#240)
* :sparkles: add support for OCR text print in CLI tool (#239)
### Fixes
* :recycle: fix miscellaneous typos (#241)


## v4.8.0 - 2024-05-24
### Changes
* :sparkles: add support for webhooks responses & HMAC validation
* :recycle: replaced PikePDF with PyPdfium2


## v4.7.0 - 2024-05-16
### Changes
* :sparkles: update receipt to 5.2 and financial document to 1.7


## v4.6.0 - 2024-04-30
### Changes
* :sparkles: add support for financial document v1.6 and invoice 4.6


## v4.5.0 - 2024-03-15
### Changes
* :sparkles: update Invoice to v4.5
### Fixes
* :bug: fix invalid error code handling for some errors (#227)


## v4.4.1 - 2024-03-05
### Changes
* :recycle: update error handling to account for future evolutions
* :memo: update some documentation


## v4.4.0 - 2024-02-21
### Changes
* :sparkles: add support for Resume V1
* :sparkles: add support for EU Driver License V1
* :sparkles: add support for International ID V2
### Fixes
* :memo: fix miscellaneous documentation issues


## v4.3.0 - 2024-01-30
### Changes
* :arrow_up: update invoices to v4.4
* :sparkles: add support for `raw_value` in string fields


## v4.2.0 - 2024-01-18
### Changes
* :sparkles: add support for International ID V1
* :sparkles: add support for Generated APIs
* :sparkles: add custom associated classes & namespace for Generated APIs
* :memo: update sample codes for default usage
* :memo: add documentation for Generated APIs

### Fixes
* :bug: fix sphinx doc from mistakenly looking for static files
* :bug: fix default async config to avoid timeouts on larger files
* :bug: fix for build badges


## v4.1.0 - 2023-10-17
### Changes
* :test_tube: optimize CI + add retry mechanism
* :recycle: homogenize typing & classes
* :arrow_up: upgrade support for python 3.12
* :sparkles: add n_pages attribute to document
* :test_tube: :sparkles: add **experimental** pdf-fixing utility

### Fixes
* :memo: fix invoice-splitter doc
* :wrench: fix wrongful instance variable assignments
* :wrench: rework custom internals & fix custom page_id

## v4.0.2 - 2023-10-11
### Fixes
* :bug: fix crashes when trying to parse from newer custom APIs


## v4.0.1 - 2023-10-30
### Fixes
* :bug: add missing internal imports for some products


## v4.0.0 - 2023-10-30
### ¡Breaking Changes!
* :art: :boom: harmonize response types & syntax with other libraries
* :art: :boom: change endpoint management & syntax
* :art: :boom: move products to `product` module

### Changes
* :sparkles: add support for auto-poll asynchronous parsing
* :sparkles: add support for products with both sync & async modes
* :sparkles: add support for async custom products
* :sparkles: :memo: add auto-generated md doc
* :recycle: :memo: update rst doc
* :arrow_up: update dependencies
* :test_tube:  add experimental support for feedback API
* :arrow_up:  improved support for custom Line Items reconstruction
* :arrow_up: update error management system
* :recycle: update unit-tests
* :arrow_up: implement regression testing
* :recycle: update CLI
* :recycle: re-organize geometry module
* :coffin: remove support for ReceiptV3
* :coffin: remove support for InvoiceV3

### Fixes
* :bug: fix `raw_http` attribute displaying a python dict instead of raw JSON


## v3.13.2 - 2023-10-18
### Changes
* :arrow_up: update `urllib` & `pillow` dependencies


## v3.13.1 - 2023-10-03
### Changes
* :arrow_up: update `urllib`, `charset-normalizer` & `package` dependencies


## v3.13.0 - 2023-09-21
### Changes
* :sparkles: add support for Multi Receipts Detector V1
* :sparkles: add support for Barcode Reader V1
* :sparkles: add support for US W9 V1
* :recycle: small internal tweaks to accomodate for new products


## v3.12.0 - 2023-09-15
### Changes
* :sparkles: add support for FR ID card v2


## v3.11.1 - 2023-07-13
### Changes
* :arrow_up: GitHub CI and mypy updates
* :arrow_up: update requests to 2.31

### Fixes
* :bug: fix full_name for multiple given names
* :bug: fix for parsing OCR response in CLI


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
