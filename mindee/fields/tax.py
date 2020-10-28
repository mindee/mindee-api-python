from mindee.fields import Field


class Tax(Field):
    def __init__(
            self,
            tax_prediction,
            value_key="amount",
            rate_key="rate",
            code_key="code",
            reconstructed=False,
            page_n=None
    ):
        """
        :param tax_prediction: Tax prediction object from HTTP response
        :param value_key: Key to use in the tax_prediction dict
        :param rate_key: Key to use for getting the Tax rate in the tax_prediction dict
        :param code_key: Key to use for getting the Tax code in the tax_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super(Tax, self).__init__(
            tax_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n
        )

        try:
            self.rate = float(tax_prediction[rate_key])
        except:
            self.rate = None

        try:
            self.code = str(tax_prediction[code_key])
            if self.code == "N/A":
                self.code = None
        except:
            self.code = None

        try:
            self.value = float(tax_prediction[value_key])
        except:
            self.value = None
            self.probability = 0.

    def __str__(self):
        tax_str = ""
        if self.value is not None:
            tax_str += str(self.value)
        else:
            tax_str += "_"

        if self.rate is not None:
            tax_str += "; "+str(self.rate)+"%"
        else:
            tax_str += "; _"

        if self.code is not None:
            tax_str += "; "+str(self.code)
        else:
            tax_str += "; _"

        return tax_str


