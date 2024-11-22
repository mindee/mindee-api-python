from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.amount import AmountField
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_added_sugar import (
    NutritionFactsLabelV1AddedSugar,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_calorie import (
    NutritionFactsLabelV1Calorie,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_cholesterol import (
    NutritionFactsLabelV1Cholesterol,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_dietary_fiber import (
    NutritionFactsLabelV1DietaryFiber,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_nutrient import (
    NutritionFactsLabelV1Nutrient,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_protein import (
    NutritionFactsLabelV1Protein,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_saturated_fat import (
    NutritionFactsLabelV1SaturatedFat,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_serving_size import (
    NutritionFactsLabelV1ServingSize,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_sodium import (
    NutritionFactsLabelV1Sodium,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_carbohydrate import (
    NutritionFactsLabelV1TotalCarbohydrate,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_fat import (
    NutritionFactsLabelV1TotalFat,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_sugar import (
    NutritionFactsLabelV1TotalSugar,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_trans_fat import (
    NutritionFactsLabelV1TransFat,
)


class NutritionFactsLabelV1Document(Prediction):
    """Nutrition Facts Label API version 1.0 document data."""

    added_sugars: NutritionFactsLabelV1AddedSugar
    """The amount of added sugars in the product."""
    calories: NutritionFactsLabelV1Calorie
    """The amount of calories in the product."""
    cholesterol: NutritionFactsLabelV1Cholesterol
    """The amount of cholesterol in the product."""
    dietary_fiber: NutritionFactsLabelV1DietaryFiber
    """The amount of dietary fiber in the product."""
    nutrients: List[NutritionFactsLabelV1Nutrient]
    """The amount of nutrients in the product."""
    protein: NutritionFactsLabelV1Protein
    """The amount of protein in the product."""
    saturated_fat: NutritionFactsLabelV1SaturatedFat
    """The amount of saturated fat in the product."""
    serving_per_box: AmountField
    """The number of servings in each box of the product."""
    serving_size: NutritionFactsLabelV1ServingSize
    """The size of a single serving of the product."""
    sodium: NutritionFactsLabelV1Sodium
    """The amount of sodium in the product."""
    total_carbohydrate: NutritionFactsLabelV1TotalCarbohydrate
    """The total amount of carbohydrates in the product."""
    total_fat: NutritionFactsLabelV1TotalFat
    """The total amount of fat in the product."""
    total_sugars: NutritionFactsLabelV1TotalSugar
    """The total amount of sugars in the product."""
    trans_fat: NutritionFactsLabelV1TransFat
    """The amount of trans fat in the product."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Nutrition Facts Label document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.added_sugars = NutritionFactsLabelV1AddedSugar(
            raw_prediction["added_sugars"],
            page_id=page_id,
        )
        self.calories = NutritionFactsLabelV1Calorie(
            raw_prediction["calories"],
            page_id=page_id,
        )
        self.cholesterol = NutritionFactsLabelV1Cholesterol(
            raw_prediction["cholesterol"],
            page_id=page_id,
        )
        self.dietary_fiber = NutritionFactsLabelV1DietaryFiber(
            raw_prediction["dietary_fiber"],
            page_id=page_id,
        )
        self.nutrients = [
            NutritionFactsLabelV1Nutrient(prediction, page_id=page_id)
            for prediction in raw_prediction["nutrients"]
        ]
        self.protein = NutritionFactsLabelV1Protein(
            raw_prediction["protein"],
            page_id=page_id,
        )
        self.saturated_fat = NutritionFactsLabelV1SaturatedFat(
            raw_prediction["saturated_fat"],
            page_id=page_id,
        )
        self.serving_per_box = AmountField(
            raw_prediction["serving_per_box"],
            page_id=page_id,
        )
        self.serving_size = NutritionFactsLabelV1ServingSize(
            raw_prediction["serving_size"],
            page_id=page_id,
        )
        self.sodium = NutritionFactsLabelV1Sodium(
            raw_prediction["sodium"],
            page_id=page_id,
        )
        self.total_carbohydrate = NutritionFactsLabelV1TotalCarbohydrate(
            raw_prediction["total_carbohydrate"],
            page_id=page_id,
        )
        self.total_fat = NutritionFactsLabelV1TotalFat(
            raw_prediction["total_fat"],
            page_id=page_id,
        )
        self.total_sugars = NutritionFactsLabelV1TotalSugar(
            raw_prediction["total_sugars"],
            page_id=page_id,
        )
        self.trans_fat = NutritionFactsLabelV1TransFat(
            raw_prediction["trans_fat"],
            page_id=page_id,
        )

    @staticmethod
    def _nutrients_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 13}"
        out_str += f"+{char * 22}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 6}"
        return out_str + "+"

    def _nutrients_to_str(self) -> str:
        if not self.nutrients:
            return ""

        lines = f"\n{self._nutrients_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.nutrients]
        )
        out_str = ""
        out_str += f"\n{self._nutrients_separator('-')}\n "
        out_str += " | Daily Value"
        out_str += " | Name                "
        out_str += " | Per 100g"
        out_str += " | Per Serving"
        out_str += " | Unit"
        out_str += f" |\n{self._nutrients_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._nutrients_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Serving per Box: {self.serving_per_box}\n"
        out_str += f":Serving Size:\n{self.serving_size.to_field_list()}\n"
        out_str += f":Calories:\n{self.calories.to_field_list()}\n"
        out_str += f":Total Fat:\n{self.total_fat.to_field_list()}\n"
        out_str += f":Saturated Fat:\n{self.saturated_fat.to_field_list()}\n"
        out_str += f":Trans Fat:\n{self.trans_fat.to_field_list()}\n"
        out_str += f":Cholesterol:\n{self.cholesterol.to_field_list()}\n"
        out_str += f":Total Carbohydrate:\n{self.total_carbohydrate.to_field_list()}\n"
        out_str += f":Dietary Fiber:\n{self.dietary_fiber.to_field_list()}\n"
        out_str += f":Total Sugars:\n{self.total_sugars.to_field_list()}\n"
        out_str += f":Added Sugars:\n{self.added_sugars.to_field_list()}\n"
        out_str += f":Protein:\n{self.protein.to_field_list()}\n"
        out_str += f":sodium:\n{self.sodium.to_field_list()}\n"
        out_str += f":nutrients: {self._nutrients_to_str()}\n"
        return clean_out_string(out_str)
