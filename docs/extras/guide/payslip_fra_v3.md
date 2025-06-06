---
title: FR Payslip OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-fr-payslip-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Payslip API](https://platform.mindee.com/mindee/payslip_fra).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/payslip_fra/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Payslip sample](https://github.com/mindee/client-lib-test-data/blob/main/products/payslip_fra/default_sample.jpg?raw=true)

# Quick-Start
```py
#
# Install the Python client library by running:
# pip install mindee
#

from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.fr.PayslipV3,
    input_doc,
)

# Print a brief summary of the parsed data
print(result.document)

```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: a479e3e7-6838-4e82-9a7d-99289f34ec7f
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/payslip_fra v3.0
:Rotation applied: Yes

Prediction
==========
:Pay Period:
  :End Date: 2023-03-31
  :Month: 03
  :Payment Date: 2023-03-29
  :Start Date: 2023-03-01
  :Year: 2023
:Employee:
  :Address: 52 RUE DES FLEURS 33500 LIBOURNE FRANCE
  :Date of Birth:
  :First Name: Jean Luc
  :Last Name: Picard
  :Phone Number:
  :Registration Number:
  :Social Security Number: 123456789012345
:Employer:
  :Address: 1 RUE DU TONNOT 25210 DOUBS
  :Company ID: 12345678901234
  :Company Site:
  :NAF Code: 1234A
  :Name: DEMO COMPANY
  :Phone Number:
  :URSSAF Number:
:Bank Account Details:
  :Bank Name:
  :IBAN:
  :SWIFT:
:Employment:
  :Category: Cadre
  :Coefficient: 600,000
  :Collective Agreement: Construction -- Promotion
  :Job Title: Directeur Régional du Développement
  :Position Level: Niveau 5 Echelon 3
  :Seniority Date:
  :Start Date: 2022-05-01
:Salary Details:
  +--------------+-----------+--------------------------------------+--------+-----------+
  | Amount       | Base      | Description                          | Number | Rate      |
  +==============+===========+======================================+========+===========+
  | 6666.67      |           | Salaire de base                      |        |           |
  +--------------+-----------+--------------------------------------+--------+-----------+
  | 9.30         |           | Part patronale Mutuelle NR           |        |           |
  +--------------+-----------+--------------------------------------+--------+-----------+
  | 508.30       |           | Avantages en nature voiture          |        |           |
  +--------------+-----------+--------------------------------------+--------+-----------+
:Pay Detail:
  :Gross Salary: 7184.27
  :Gross Salary YTD: 18074.81
  :Income Tax Rate: 17.60
  :Income Tax Withheld: 1030.99
  :Net Paid: 3868.32
  :Net Paid Before Tax: 4899.31
  :Net Taxable: 5857.90
  :Net Taxable YTD: 14752.73
  :Total Cost Employer: 10486.94
  :Total Taxes and Deductions: 1650.36
:Paid Time Off:
  +-----------+--------+-------------+-----------+-----------+
  | Accrued   | Period | Type        | Remaining | Used      |
  +===========+========+=============+===========+===========+
  |           | N-1    | VACATION    |           |           |
  +-----------+--------+-------------+-----------+-----------+
  | 6.17      | N      | VACATION    | 6.17      |           |
  +-----------+--------+-------------+-----------+-----------+
  | 2.01      | N      | RTT         | 2.01      |           |
  +-----------+--------+-------------+-----------+-----------+
```

# Field Types
## Standard Fields
These fields are generic and used in several products.

### BaseField
Each prediction object contains a set of fields that inherit from the generic `BaseField` class.
A typical `BaseField` object will have the following attributes:

* **value** (`Union[float, str]`): corresponds to the field value. Can be `None` if no value was extracted.
* **confidence** (`float`): the confidence score of the field prediction.
* **bounding_box** (`[Point, Point, Point, Point]`): contains exactly 4 relative vertices (points) coordinates of a right rectangle containing the field in the document.
* **polygon** (`List[Point]`): contains the relative vertices coordinates (`Point`) of a polygon containing the field in the image.
* **page_id** (`int`): the ID of the page, always `None` when at document-level.
* **reconstructed** (`bool`): indicates whether an object was reconstructed (not extracted as the API gave it).

> **Note:** A `Point` simply refers to a List of two numbers (`[float, float]`).


Aside from the previous attributes, all basic fields have access to a custom `__str__` method that can be used to print their value as a string.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Bank Account Details Field
Information about the employee's bank account.

A `PayslipV3BankAccountDetail` implements the following attributes:

* **bank_name** (`str`): The name of the bank.
* **iban** (`str`): The IBAN of the bank account.
* **swift** (`str`): The SWIFT code of the bank.
Fields which are specific to this product; they are not used in any other product.

### Employee Field
Information about the employee.

A `PayslipV3Employee` implements the following attributes:

* **address** (`str`): The address of the employee.
* **date_of_birth** (`str`): The date of birth of the employee.
* **first_name** (`str`): The first name of the employee.
* **last_name** (`str`): The last name of the employee.
* **phone_number** (`str`): The phone number of the employee.
* **registration_number** (`str`): The registration number of the employee.
* **social_security_number** (`str`): The social security number of the employee.
Fields which are specific to this product; they are not used in any other product.

### Employer Field
Information about the employer.

A `PayslipV3Employer` implements the following attributes:

* **address** (`str`): The address of the employer.
* **company_id** (`str`): The company ID of the employer.
* **company_site** (`str`): The site of the company.
* **naf_code** (`str`): The NAF code of the employer.
* **name** (`str`): The name of the employer.
* **phone_number** (`str`): The phone number of the employer.
* **urssaf_number** (`str`): The URSSAF number of the employer.
Fields which are specific to this product; they are not used in any other product.

### Employment Field
Information about the employment.

A `PayslipV3Employment` implements the following attributes:

* **category** (`str`): The category of the employment.
* **coefficient** (`str`): The coefficient of the employment.
* **collective_agreement** (`str`): The collective agreement of the employment.
* **job_title** (`str`): The job title of the employee.
* **position_level** (`str`): The position level of the employment.
* **seniority_date** (`str`): The seniority date of the employment.
* **start_date** (`str`): The start date of the employment.
Fields which are specific to this product; they are not used in any other product.

### Paid Time Off Field
Information about paid time off.

A `PayslipV3PaidTimeOff` implements the following attributes:

* **accrued** (`float`): The amount of paid time off accrued in the period.
* **period** (`str`): The paid time off period.

#### Possible values include:
 - N
 - N-1
 - N-2

* **pto_type** (`str`): The type of paid time off.

#### Possible values include:
 - VACATION
 - RTT
 - COMPENSATORY

* **remaining** (`float`): The remaining amount of paid time off at the end of the period.
* **used** (`float`): The amount of paid time off used in the period.
Fields which are specific to this product; they are not used in any other product.

### Pay Detail Field
Detailed information about the pay.

A `PayslipV3PayDetail` implements the following attributes:

* **gross_salary** (`float`): The gross salary of the employee.
* **gross_salary_ytd** (`float`): The year-to-date gross salary of the employee.
* **income_tax_rate** (`float`): The income tax rate of the employee.
* **income_tax_withheld** (`float`): The income tax withheld from the employee's pay.
* **net_paid** (`float`): The net paid amount of the employee.
* **net_paid_before_tax** (`float`): The net paid amount before tax of the employee.
* **net_taxable** (`float`): The net taxable amount of the employee.
* **net_taxable_ytd** (`float`): The year-to-date net taxable amount of the employee.
* **total_cost_employer** (`float`): The total cost to the employer.
* **total_taxes_and_deductions** (`float`): The total taxes and deductions of the employee.
Fields which are specific to this product; they are not used in any other product.

### Pay Period Field
Information about the pay period.

A `PayslipV3PayPeriod` implements the following attributes:

* **end_date** (`str`): The end date of the pay period.
* **month** (`str`): The month of the pay period.
* **payment_date** (`str`): The date of payment for the pay period.
* **start_date** (`str`): The start date of the pay period.
* **year** (`str`): The year of the pay period.
Fields which are specific to this product; they are not used in any other product.

### Salary Details Field
Detailed information about the earnings.

A `PayslipV3SalaryDetail` implements the following attributes:

* **amount** (`float`): The amount of the earning.
* **base** (`float`): The base rate value of the earning.
* **description** (`str`): The description of the earnings.
* **number** (`float`): The number of units in the earning.
* **rate** (`float`): The rate of the earning.

# Attributes
The following fields are extracted for Payslip V3:

## Bank Account Details
**bank_account_details** ([PayslipV3BankAccountDetail](#bank-account-details-field)): Information about the employee's bank account.

```py
print(result.document.inference.prediction.bank_account_details.value)
```

## Employee
**employee** ([PayslipV3Employee](#employee-field)): Information about the employee.

```py
print(result.document.inference.prediction.employee.value)
```

## Employer
**employer** ([PayslipV3Employer](#employer-field)): Information about the employer.

```py
print(result.document.inference.prediction.employer.value)
```

## Employment
**employment** ([PayslipV3Employment](#employment-field)): Information about the employment.

```py
print(result.document.inference.prediction.employment.value)
```

## Paid Time Off
**paid_time_off** (List[[PayslipV3PaidTimeOff](#paid-time-off-field)]): Information about paid time off.

```py
for paid_time_off_elem in result.document.inference.prediction.paid_time_off:
    print(paid_time_off_elem.value)
```

## Pay Detail
**pay_detail** ([PayslipV3PayDetail](#pay-detail-field)): Detailed information about the pay.

```py
print(result.document.inference.prediction.pay_detail.value)
```

## Pay Period
**pay_period** ([PayslipV3PayPeriod](#pay-period-field)): Information about the pay period.

```py
print(result.document.inference.prediction.pay_period.value)
```

## Salary Details
**salary_details** (List[[PayslipV3SalaryDetail](#salary-details-field)]): Detailed information about the earnings.

```py
for salary_details_elem in result.document.inference.prediction.salary_details:
    print(salary_details_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
