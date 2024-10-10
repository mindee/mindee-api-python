---
title: Nutrition Facts Label OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-nutrition-facts-label-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Nutrition Facts Label API](https://platform.mindee.com/mindee/nutrition_facts).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/nutrition_facts/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Nutrition Facts Label sample](https://github.com/mindee/client-lib-test-data/blob/main/products/nutrition_facts/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.NutritionFactsLabelV1,
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
:Mindee ID: 38a12fe0-5d69-4ca4-9b30-12f1b659311c
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/nutrition_facts v1.0
:Rotation applied: No

Prediction
==========
:Serving per Box: 2.00
:Serving Size:
  :Amount: 228.00
  :Unit: g
:Calories:
  :Daily Value:
  :Per 100g:
  :Per Serving: 250.00
:Total Fat:
  :Daily Value:
  :Per 100g:
  :Per Serving: 12.00
:Saturated Fat:
  :Daily Value: 15.00
  :Per 100g:
  :Per Serving: 3.00
:Trans Fat:
  :Daily Value:
  :Per 100g:
  :Per Serving: 3.00
:Cholesterol:
  :Daily Value: 10.00
  :Per 100g:
  :Per Serving: 30.00
:Total Carbohydrate:
  :Daily Value: 10.00
  :Per 100g:
  :Per Serving: 31.00
:Dietary Fiber:
  :Daily Value: 0.00
  :Per 100g:
  :Per Serving: 0.00
:Total Sugars:
  :Daily Value:
  :Per 100g:
  :Per Serving: 5.00
:Added Sugars:
  :Daily Value:
  :Per 100g:
  :Per Serving:
:Protein:
  :Daily Value:
  :Per 100g:
  :Per Serving: 5.00
:sodium:
  :Daily Value: 20.00
  :Per 100g:
  :Per Serving: 470.00
  :Unit: mg
:nutrients:
  +-------------+----------------------+----------+-------------+------+
  | Daily Value | Name                 | Per 100g | Per Serving | Unit |
  +=============+======================+==========+=============+======+
  | 12.00       | Vitamin A            |          | 4.00        | mcg  |
  +-------------+----------------------+----------+-------------+------+
  | 12.00       | Vitamin C            |          | 2.00        | mg   |
  +-------------+----------------------+----------+-------------+------+
  | 12.00       | Calcium              |          | 45.60       | mg   |
  +-------------+----------------------+----------+-------------+------+
  | 12.00       | Iron                 |          | 0.90        | mg   |
  +-------------+----------------------+----------+-------------+------+
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


### AmountField
The amount field `AmountField` only has one constraint: its **value** is an `Optional[float]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Added Sugars Field
The amount of added sugars in the product.

A `NutritionFactsLabelV1AddedSugar` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of added sugars to consume or not to exceed each day.
* **per_100g** (`float`): The amount of added sugars per 100g of the product.
* **per_serving** (`float`): The amount of added sugars per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Calories Field
The amount of calories in the product.

A `NutritionFactsLabelV1Calorie` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of calories to consume or not to exceed each day.
* **per_100g** (`float`): The amount of calories per 100g of the product.
* **per_serving** (`float`): The amount of calories per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Cholesterol Field
The amount of cholesterol in the product.

A `NutritionFactsLabelV1Cholesterol` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of cholesterol to consume or not to exceed each day.
* **per_100g** (`float`): The amount of cholesterol per 100g of the product.
* **per_serving** (`float`): The amount of cholesterol per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Dietary Fiber Field
The amount of dietary fiber in the product.

A `NutritionFactsLabelV1DietaryFiber` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of dietary fiber to consume or not to exceed each day.
* **per_100g** (`float`): The amount of dietary fiber per 100g of the product.
* **per_serving** (`float`): The amount of dietary fiber per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### nutrients Field
The amount of nutrients in the product.

A `NutritionFactsLabelV1Nutrient` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of nutrients to consume or not to exceed each day.
* **name** (`str`): The name of nutrients of the product.
* **per_100g** (`float`): The amount of nutrients per 100g of the product.
* **per_serving** (`float`): The amount of nutrients per serving of the product.
* **unit** (`str`): The unit of measurement for the amount of nutrients.
Fields which are specific to this product; they are not used in any other product.

### Protein Field
The amount of protein in the product.

A `NutritionFactsLabelV1Protein` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of protein to consume or not to exceed each day.
* **per_100g** (`float`): The amount of protein per 100g of the product.
* **per_serving** (`float`): The amount of protein per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Saturated Fat Field
The amount of saturated fat in the product.

A `NutritionFactsLabelV1SaturatedFat` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of saturated fat to consume or not to exceed each day.
* **per_100g** (`float`): The amount of saturated fat per 100g of the product.
* **per_serving** (`float`): The amount of saturated fat per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Serving Size Field
The size of a single serving of the product.

A `NutritionFactsLabelV1ServingSize` implements the following attributes:

* **amount** (`float`): The amount of a single serving.
* **unit** (`str`): The unit for the amount of a single serving.
Fields which are specific to this product; they are not used in any other product.

### sodium Field
The amount of sodium in the product.

A `NutritionFactsLabelV1Sodium` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of sodium to consume or not to exceed each day.
* **per_100g** (`float`): The amount of sodium per 100g of the product.
* **per_serving** (`float`): The amount of sodium per serving of the product.
* **unit** (`str`): The unit of measurement for the amount of sodium.
Fields which are specific to this product; they are not used in any other product.

### Total Carbohydrate Field
The total amount of carbohydrates in the product.

A `NutritionFactsLabelV1TotalCarbohydrate` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of total carbohydrates to consume or not to exceed each day.
* **per_100g** (`float`): The amount of total carbohydrates per 100g of the product.
* **per_serving** (`float`): The amount of total carbohydrates per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Total Fat Field
The total amount of fat in the product.

A `NutritionFactsLabelV1TotalFat` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of total fat to consume or not to exceed each day.
* **per_100g** (`float`): The amount of total fat per 100g of the product.
* **per_serving** (`float`): The amount of total fat per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Total Sugars Field
The total amount of sugars in the product.

A `NutritionFactsLabelV1TotalSugar` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of total sugars to consume or not to exceed each day.
* **per_100g** (`float`): The amount of total sugars per 100g of the product.
* **per_serving** (`float`): The amount of total sugars per serving of the product.
Fields which are specific to this product; they are not used in any other product.

### Trans Fat Field
The amount of trans fat in the product.

A `NutritionFactsLabelV1TransFat` implements the following attributes:

* **daily_value** (`float`): DVs are the recommended amounts of trans fat to consume or not to exceed each day.
* **per_100g** (`float`): The amount of trans fat per 100g of the product.
* **per_serving** (`float`): The amount of trans fat per serving of the product.

# Attributes
The following fields are extracted for Nutrition Facts Label V1:

## Added Sugars
**added_sugars** ([NutritionFactsLabelV1AddedSugar](#added-sugars-field)): The amount of added sugars in the product.

```py
print(result.document.inference.prediction.added_sugars.value)
```

## Calories
**calories** ([NutritionFactsLabelV1Calorie](#calories-field)): The amount of calories in the product.

```py
print(result.document.inference.prediction.calories.value)
```

## Cholesterol
**cholesterol** ([NutritionFactsLabelV1Cholesterol](#cholesterol-field)): The amount of cholesterol in the product.

```py
print(result.document.inference.prediction.cholesterol.value)
```

## Dietary Fiber
**dietary_fiber** ([NutritionFactsLabelV1DietaryFiber](#dietary-fiber-field)): The amount of dietary fiber in the product.

```py
print(result.document.inference.prediction.dietary_fiber.value)
```

## nutrients
**nutrients** (List[[NutritionFactsLabelV1Nutrient](#nutrients-field)]): The amount of nutrients in the product.

```py
for nutrients_elem in result.document.inference.prediction.nutrients:
    print(nutrients_elem.value)
```

## Protein
**protein** ([NutritionFactsLabelV1Protein](#protein-field)): The amount of protein in the product.

```py
print(result.document.inference.prediction.protein.value)
```

## Saturated Fat
**saturated_fat** ([NutritionFactsLabelV1SaturatedFat](#saturated-fat-field)): The amount of saturated fat in the product.

```py
print(result.document.inference.prediction.saturated_fat.value)
```

## Serving per Box
**serving_per_box** ([AmountField](#amountfield)): The number of servings in each box of the product.

```py
print(result.document.inference.prediction.serving_per_box.value)
```

## Serving Size
**serving_size** ([NutritionFactsLabelV1ServingSize](#serving-size-field)): The size of a single serving of the product.

```py
print(result.document.inference.prediction.serving_size.value)
```

## sodium
**sodium** ([NutritionFactsLabelV1Sodium](#sodium-field)): The amount of sodium in the product.

```py
print(result.document.inference.prediction.sodium.value)
```

## Total Carbohydrate
**total_carbohydrate** ([NutritionFactsLabelV1TotalCarbohydrate](#total-carbohydrate-field)): The total amount of carbohydrates in the product.

```py
print(result.document.inference.prediction.total_carbohydrate.value)
```

## Total Fat
**total_fat** ([NutritionFactsLabelV1TotalFat](#total-fat-field)): The total amount of fat in the product.

```py
print(result.document.inference.prediction.total_fat.value)
```

## Total Sugars
**total_sugars** ([NutritionFactsLabelV1TotalSugar](#total-sugars-field)): The total amount of sugars in the product.

```py
print(result.document.inference.prediction.total_sugars.value)
```

## Trans Fat
**trans_fat** ([NutritionFactsLabelV1TransFat](#trans-fat-field)): The amount of trans fat in the product.

```py
print(result.document.inference.prediction.trans_fat.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
