The Python  OCR SDK supports the [passport API](https://developers.mindee.com/docs/passport-ocr) for extracting data from passports.

```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the Passport by passing the appropriate type
result = input_doc.parse(product.TypePassportV1)

# Print a brief summary of the parsed data
print(result.document)
```

Using this sample fake passport below, we are going to illustrate how to extract the data that we want using the SDK.
![fake passport](https://files.readme.io/4a16b1d-passport_pic.jpg)

## Passport Data Structure
The passport object JSON data structure consists of:

- [Document level prediction](#document-level-prediction)
- [Page level prediction](#page-level-prediction)
- [Raw HTTP response](#raw-http-response)

### Document Level Prediction
For document level prediction, we construct the document class by combining the different pages in a single document.
This method used for creating a single passport object from multiple pages relies on **field confidence scores**.

Basically, we iterate over each page, and for each field, we keep the one that has the highest probability.

For example, if you send a three-page passport, the document level will provide you with one name, one country code, and so on.

```python
print(api_response.document)
```

Output:
```
-----Passport data-----
Filename: passport.jpeg
Full name: HENERT PUDARSAN
Given names: HENERT
Surname: PUDARSAN
Country: GBR
ID Number: 707797979
Issuance date: 2012-04-22
Birth date: 1995-05-20
Expiry date: 2017-04-22
MRZ 1: P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<
MRZ 2: 7077979792GBR9505209M1704224<<<<<<<<<<<<<<00
MRZ: P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<7077979792GBR9505209M1704224<<<<<<<<<<<<<<00
----------------------
```

### Page level prediction

We create the document class by iterating over each page one by one. Each page in the pdf is treated as a unique page.

For example, if you send a three-page passport, the page-level prediction will provide you with three names, three-countries codes, and so on.

```python
print(result.pages)
```

### Raw HTTP Response
Contains the full Mindee API HTTP response object in JSON format

```python
result.http_response # full HTTP request object
```


## Extracted Fields
Each passport object contains a set of different fields. Each field contains the four following attributes:

- **value** (Str or Float depending on the field type): corresponds to the field value. Set to None if the `field` was not extracted.
- **probability** (Float): the confidence score of the field prediction.
- **bounding_box** (Array[Float]): contains the relative vertices coordinates of the bounding box containing the `field` in the image.
  If the field is not written, the `bbox` is an empty array.
- **reconstructed** (Bool): `True` if the field was reconstructed using other fields.


### Additional Attributes
Depending on the field type specified, additional attributes can be extracted from the passport object.

Using the above example, the following are the basic fields that can be extracted.

- [Birth Information](#birth-information)
- [Country](#country)
- [Date](#date)
- [Gender](#gender)
- [Given Names](#given-names)
- [ID Number](#id)
- [Issuance Date](#issuance-date)
- [Machine Readable Zone](#machine-readable-zone)
- [Surname](#surname)

### Birth Information
- **birth_date** (string): Passport's owner date of birth.

```python
# To get the passport's owner date of birth
birth_date = result.document.birth_date.value
print("DOB: ", birth_date)
```

- **birth_place** (string): Passport owner birthplace.

```python
# To get the passport's owner
birth_place = result.document.birth_place.value
print("birthplace: ", birth_place)
```

### Country
- **country** (string): Passport country in [ISO 3166-1 alpha-3 code format](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) (3 letters code).

```python
# To get the passport country code
country_code = result.document.country.value
print("passport country code: ", country_code)
```

### Date
- **expiry_date** (string): Passport expiry date in [ISO format](https://en.wikipedia.org/wiki/ISO_8601) (yyyy-mm-dd).

```python
# To get the passport expiry date
expiry_date = result.document.expiry_date.value
print("expires: ", expiry_date)
```

### Gender
- **gender** (string): Passport's owner gender (M / F).

```python
# To get the passport's owner gender (string among {"M", "F"}
gender = result.document.gender.value
print("gender: ", gender)
```

### Given Names
- **given_names** (string): List of passport's owner given names.

```python
# To get the list of names
given_names = result.document.given_names
print("Given names: ")
# Loop on each given name
for given_name in given_names:
   # To get the name string
   name = given_name.value
print(name)
```

### ID
- **id_number** (string): Passport identification number.

```python
# To get the passport id number (string)
id_number = result.document.id_number.value
print("passport number: ", id_number)
```

### Issuance Date
- **issuance_date** (string): Passport date of issuance in [ISO format](https://en.wikipedia.org/wiki/ISO_8601) (yyyy-mm-dd).

```python
# To get the passport date of issuance
issuance_date = result.document.issuance_date.value
print("issued: ", issuance_date)
```

### Machine Readable Zone
- **mrz1** (string): Passport first line of machine-readable zone.

```python
# To get the passport  first line of machine readable zone (string)
mrz1 = result.document.mrz1.value
print("mrz1: ", mrz1)
```

- **mrz2** (string): Passport second line of machine-readable zone.

```python
# To get the passport full machine-readable zone (string)
mrz2 = result.document.mrz2.value
print("mrz2: ", mrz2)
```

- **mrz** (string): Reconstructed passport full machine readable zone from mrz1 and mrz2.

```python
# To get the passport full machine readable zone (string)
mrz = result.document.mrz
print("mrz: ", mrz)
```

### Surname
- **surname** (string): Passport's owner surname.

```python
# To get the passport's owner surname
surname = result.document.surname.value
print("surname: ", surname)
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
