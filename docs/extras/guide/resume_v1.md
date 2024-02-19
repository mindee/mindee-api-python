---
title: Resume OCR Python
---
The Python OCR SDK supports the [Resume API](https://platform.mindee.com/mindee/resume).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/resume/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Resume sample](https://github.com/mindee/client-lib-test-data/blob/main/products/resume/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse
from time import sleep

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
```

# Field Types
## Standard Fields
These fields are generic and used in several products.

### BasicField
Each prediction object contains a set of fields that inherit from the generic `BaseField` class.
A typical `BaseField` object will have the following attributes:

* **value** (`Union[float, str]`): corresponds to the field value. Can be `None` if no value was extracted.
* **confidence** (`float`): the confidence score of the field prediction.
* **bounding_box** (`[Point, Point, Point, Point]`): contains exactly 4 relative vertices (points) coordinates of a right rectangle containing the field in the document.
* **polygon** (`List[Point]`): contains the relative vertices coordinates (`Point`) of a polygon containing the field in the image.
* **page_id** (`int`): the ID of the page, is `None` when at document-level.
* **reconstructed** (`bool`): indicates whether an object was reconstructed (not extracted as the API gave it).

> **Note:** A `Point` simply refers to a List of two numbers (`[float, float]`).


Aside from the previous attributes, all basic fields have access to a custom `__str__` method that can be used to print their value as a string.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Certificates Field
The list of certificates obtained by the candidate.

A `ResumeV1Certificate` implements the following attributes:

* **grade** (`str`): The grade obtained for the certificate.
* **name** (`str`): The name of certifications obtained by the individual.
* **provider** (`str`): The organization or institution that issued the certificates listed in the document.
* **year** (`str`): The year when a certificate was issued or received.
Fields which are specific to this product; they are not used in any other product.

### Education Field
The list of values that represent the educational background of an individual.

A `ResumeV1Education` implements the following attributes:

* **degree_domain** (`str`): The area of study or specialization pursued by an individual in their educational background.
* **degree_type** (`str`): The type of degree obtained by the individual, such as Bachelor's, Master's, or Doctorate.
* **end_month** (`str`): The month when the education program or course was completed or is expected to be completed.
* **end_year** (`str`): The year when the education program or course was completed or is expected to be completed.
* **school** (`str`): The name of the school the individual went to.
* **start_month** (`str`): The month when the education program or course began.
* **start_year** (`str`): The year when the education program or course began.
Fields which are specific to this product; they are not used in any other product.

### Languages Field
The list of languages that a person is proficient in, as stated in their resume.

A `ResumeV1Language` implements the following attributes:

* **language** (`str`): The language ISO 639 code.
* **level** (`str`): The level for the language. Possible values: 'Fluent', 'Proficient', 'Intermediate' and 'Beginner'.
Fields which are specific to this product; they are not used in any other product.

### Professional Experiences Field
The list of values that represent the professional experiences of an individual in their global resume.

A `ResumeV1ProfessionalExperience` implements the following attributes:

* **contract_type** (`str`): The type of contract for a professional experience. Possible values: 'Full-Time', 'Part-Time', 'Internship' and 'Freelance'.
* **department** (`str`): The specific department or division within a company where the professional experience was gained.
* **employer** (`str`): The name of the company or organization where the candidate has worked.
* **end_month** (`str`): The month when a professional experience ended.
* **end_year** (`str`): The year when a professional experience ended.
* **role** (`str`): The position or job title held by the individual in their previous work experience.
* **start_month** (`str`): The month when a professional experience began.
* **start_year** (`str`): The year when a professional experience began.
Fields which are specific to this product; they are not used in any other product.

### Social Networks Field
The list of URLs for social network profiles of the person.

A `ResumeV1SocialNetworksUrl` implements the following attributes:

* **name** (`str`): The name of of the social media concerned.
* **url** (`str`): The URL of the profile for this particular social network.

# Attributes
The following fields are extracted for Resume V1:

## Address
**address** ([StringField](#stringfield)): The location information of the person, including city, state, and country.

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
**document_type** ([StringField](#stringfield)): The type of the document sent, possible values being RESUME, MOTIVATION_LETTER and RECOMMENDATION_LETTER.

```py
print(result.document.inference.prediction.document_type.value)
```

## Education
**education** (List[[ResumeV1Education](#education-field)]): The list of values that represent the educational background of an individual.

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
**given_names** (List[[StringField](#stringfield)]): The list of names that represent a person's first or given names.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## Hard Skills
**hard_skills** (List[[StringField](#stringfield)]): The list of specific technical abilities and knowledge mentioned in a resume.

```py
for hard_skills_elem in result.document.inference.prediction.hard_skills:
    print(hard_skills_elem.value)
```

## Job Applied
**job_applied** ([StringField](#stringfield)): The specific industry or job role that the applicant is applying for.

```py
print(result.document.inference.prediction.job_applied.value)
```

## Languages
**languages** (List[[ResumeV1Language](#languages-field)]): The list of languages that a person is proficient in, as stated in their resume.

```py
for languages_elem in result.document.inference.prediction.languages:
    print(languages_elem.value)
```

## Nationality
**nationality** ([StringField](#stringfield)): The ISO 3166 code for the country of citizenship or origin of the person.

```py
print(result.document.inference.prediction.nationality.value)
```

## Phone Number
**phone_number** ([StringField](#stringfield)): The phone number of the candidate.

```py
print(result.document.inference.prediction.phone_number.value)
```

## Profession
**profession** ([StringField](#stringfield)): The area of expertise or specialization in which the individual has professional experience and qualifications.

```py
print(result.document.inference.prediction.profession.value)
```

## Professional Experiences
**professional_experiences** (List[[ResumeV1ProfessionalExperience](#professional-experiences-field)]): The list of values that represent the professional experiences of an individual in their global resume.

```py
for professional_experiences_elem in result.document.inference.prediction.professional_experiences:
    print(professional_experiences_elem.value)
```

## Social Networks
**social_networks_urls** (List[[ResumeV1SocialNetworksUrl](#social-networks-field)]): The list of URLs for social network profiles of the person.

```py
for social_networks_urls_elem in result.document.inference.prediction.social_networks_urls:
    print(social_networks_urls_elem.value)
```

## Soft Skills
**soft_skills** (List[[StringField](#stringfield)]): The list of values that represent a person's interpersonal and communication abilities in a global resume.

```py
for soft_skills_elem in result.document.inference.prediction.soft_skills:
    print(soft_skills_elem.value)
```

## Surnames
**surnames** (List[[StringField](#stringfield)]): The list of last names provided in a resume document.

```py
for surnames_elem in result.document.inference.prediction.surnames:
    print(surnames_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
