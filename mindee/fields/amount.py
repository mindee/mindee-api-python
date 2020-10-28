from mindee.fields import Field


class Amount(Field):
    def __init__(
            self,
            amount_prediction,
            value_key="amount",
            reconstructed=False,
            page_n=None
    ):
        """
        :param amount_prediction: Amount prediction object from HTTP response
        :param value_key: Key to use in the amount_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super(Amount, self).__init__(
            amount_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n
        )

        try:
            self.value = round(float(amount_prediction[value_key]), 3)
        except:
            self.value = None
            self.probability = 0.
