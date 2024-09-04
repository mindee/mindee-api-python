---
title: Resume OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-resume-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Resume API](https://platform.mindee.com/mindee/resume).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/resume/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Resume sample](https://github.com/mindee/client-lib-test-data/blob/main/products/resume/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.ResumeV1,
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
:Mindee ID: bc80bae0-af75-4464-95a9-2419403c75bf
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/resume v1.0
:Rotation applied: No

Prediction
==========
:Document Language: ENG
:Document Type: RESUME
:Given Names: Christopher
:Surnames: Morgan
:Nationality:
:Email Address: christoper.m@gmail.com
:Phone Number: +44 (0) 20 7666 8555
:Address: 177 Great Portland Street, London W5W 6PQ
:Social Networks:
  +----------------------+----------------------------------------------------+
  | Name                 | URL                                                |
  +======================+====================================================+
  | LinkedIn             | linkedin.com/christopher.morgan                    |
  +----------------------+----------------------------------------------------+
:Profession: Senior Web Developer
:Job Applied:
:Languages:
  +----------+----------------------+
  | Language | Level                |
  +==========+======================+
  | SPA      | Fluent               |
  +----------+----------------------+
  | ZHO      | Beginner             |
  +----------+----------------------+
  | DEU      | Intermediate         |
  +----------+----------------------+
:Hard Skills: HTML5
              PHP OOP
              JavaScript
              CSS
              MySQL
:Soft Skills: Project management
              Strong decision maker
              Innovative
              Complex problem solver
              Creative design
              Service-focused
:Education:
  +-----------------+---------------------------+-----------+----------+---------------------------+-------------+------------+
  | Domain          | Degree                    | End Month | End Year | School                    | Start Month | Start Year |
  +=================+===========================+===========+==========+===========================+=============+============+
  | Computer Inf... | Bachelor                  |           |          | Columbia University, NY   |             | 2014       |
  +-----------------+---------------------------+-----------+----------+---------------------------+-------------+------------+
:Professional Experiences:
  +-----------------+------------+---------------------------+-----------+----------+----------------------+-------------+------------+
  | Contract Type   | Department | Employer                  | End Month | End Year | Role                 | Start Month | Start Year |
  +=================+============+===========================+===========+==========+======================+=============+============+
  | Full-Time       |            | Luna Web Design, New York | 05        | 2019     | Web Developer        | 09          | 2015       |
  +-----------------+------------+---------------------------+-----------+----------+----------------------+-------------+------------+
:Certificates:
  +------------+--------------------------------+---------------------------+------+
  | Grade      | Name                           | Provider                  | Year |
  +============+================================+===========================+======+
  |            | PHP Framework (certificate)... |                           | 2014 |
  +------------+--------------------------------+---------------------------+------+
  |            | Programming Languages: Java... |                           |      |
  +------------+--------------------------------+---------------------------+------+
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


### ClassificationField
The classification field `ClassificationField` does not implement all the basic `BaseField` attributes. It only implements **value**, **confidence** and **page_id**.

> Note: a classification field's `value is always a `str`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Certificates Field
The list of certificates obtained by the candidate.

A `ResumeV1Certificate` implements the following attributes:

* **grade** (`str`): The grade obtained for the certificate.
* **name** (`str`): The name of certification.
* **provider** (`str`): The organization or institution that issued the certificate.
* **year** (`str`): The year when a certificate was issued or received.
Fields which are specific to this product; they are not used in any other product.

### Education Field
The list of the candidate's educational background.

A `ResumeV1Education` implements the following attributes:

* **degree_domain** (`str`): The area of study or specialization.
* **degree_type** (`str`): The type of degree obtained, such as Bachelor's, Master's, or Doctorate.
* **end_month** (`str`): The month when the education program or course was completed.
* **end_year** (`str`): The year when the education program or course was completed.
* **school** (`str`): The name of the school.
* **start_month** (`str`): The month when the education program or course began.
* **start_year** (`str`): The year when the education program or course began.
Fields which are specific to this product; they are not used in any other product.

### Languages Field
The list of languages that the candidate is proficient in.

A `ResumeV1Language` implements the following attributes:

* **language** (`str`): The language's ISO 639 code.
* **level** (`str`): The candidate's level for the language.

#### Possible values include:
 - Fluent
 - Proficient
 - Intermediate
 - Beginner

Fields which are specific to this product; they are not used in any other product.

### Professional Experiences Field
The list of the candidate's professional experiences.

A `ResumeV1ProfessionalExperience` implements the following attributes:

* **contract_type** (`str`): The type of contract for the professional experience.

#### Possible values include:
 - Full-Time
 - Part-Time
 - Internship
 - Freelance

* **department** (`str`): The specific department or division within the company.
* **employer** (`str`): The name of the company or organization.
* **end_month** (`str`): The month when the professional experience ended.
* **end_year** (`str`): The year when the professional experience ended.
* **role** (`str`): The position or job title held by the candidate.
* **start_month** (`str`): The month when the professional experience began.
* **start_year** (`str`): The year when the professional experience began.
Fields which are specific to this product; they are not used in any other product.

### Social Networks Field
The list of social network profiles of the candidate.

A `ResumeV1SocialNetworksUrl` implements the following attributes:

* **name** (`str`): The name of the social network.
* **url** (`str`): The URL of the social network.

# Attributes
The following fields are extracted for Resume V1:

## Address
**address** ([StringField](#stringfield)): The location information of the candidate, including city, state, and country.

```py
print(result.document.inference.prediction.address.value)
```

## Certificates
**certificates** (List[[ResumeV1Certificate](#certificates-field)]): The list of certificates obtained by the candidate.

```py
for certificates_elem in result.document.inference.prediction.certificates:
    print(certificates_elem.value)
```

## Document Language
**document_language** ([StringField](#stringfield)): The ISO 639 code of the language in which the document is written.

```py
print(result.document.inference.prediction.document_language.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): The type of the document sent.

#### Possible values include:
 - RESUME
 - MOTIVATION_LETTER
 - RECOMMENDATION_LETTER

```py
print(result.document.inference.prediction.document_type.value)
```

## Education
**education** (List[[ResumeV1Education](#education-field)]): The list of the candidate's educational background.

```py
for education_elem in result.document.inference.prediction.education:
    print(education_elem.value)
```

## Email Address
**email_address** ([StringField](#stringfield)): The email address of the candidate.

```py
print(result.document.inference.prediction.email_address.value)
```

## Given Names
**given_names** (List[[StringField](#stringfield)]): The candidate's first or given names.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## Hard Skills
**hard_skills** (List[[StringField](#stringfield)]): The list of the candidate's technical abilities and knowledge.

```py
for hard_skills_elem in result.document.inference.prediction.hard_skills:
    print(hard_skills_elem.value)
```

## Job Applied
**job_applied** ([StringField](#stringfield)): The position that the candidate is applying for.

```py
print(result.document.inference.prediction.job_applied.value)
```

## Languages
**languages** (List[[ResumeV1Language](#languages-field)]): The list of languages that the candidate is proficient in.

```py
for languages_elem in result.document.inference.prediction.languages:
    print(languages_elem.value)
```

## Nationality
**nationality** ([StringField](#stringfield)): The ISO 3166 code for the country of citizenship of the candidate.

```py
print(result.document.inference.prediction.nationality.value)
```

## Phone Number
**phone_number** ([StringField](#stringfield)): The phone number of the candidate.

```py
print(result.document.inference.prediction.phone_number.value)
```

## Profession
**profession** ([StringField](#stringfield)): The candidate's current profession.

```py
print(result.document.inference.prediction.profession.value)
```

## Professional Experiences
**professional_experiences** (List[[ResumeV1ProfessionalExperience](#professional-experiences-field)]): The list of the candidate's professional experiences.

```py
for professional_experiences_elem in result.document.inference.prediction.professional_experiences:
    print(professional_experiences_elem.value)
```

## Social Networks
**social_networks_urls** (List[[ResumeV1SocialNetworksUrl](#social-networks-field)]): The list of social network profiles of the candidate.

```py
for social_networks_urls_elem in result.document.inference.prediction.social_networks_urls:
    print(social_networks_urls_elem.value)
```

## Soft Skills
**soft_skills** (List[[StringField](#stringfield)]): The list of the candidate's interpersonal and communication abilities.

```py
for soft_skills_elem in result.document.inference.prediction.soft_skills:
    print(soft_skills_elem.value)
```

## Surnames
**surnames** (List[[StringField](#stringfield)]): The candidate's last names.

```py
for surnames_elem in result.document.inference.prediction.surnames:
    print(surnames_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
