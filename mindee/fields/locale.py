from mindee.fields import Field


class Locale(Field):
    def __init__(
            self,
            locale_prediction,
            value_key="value",
            reconstructed=False,
            page_n=None
    ):
        """
        :param locale_prediction: Locale prediction object from HTTP response
        :param value_key: Key to use in the locale_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super(Locale, self).__init__(
            locale_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n
        )

        if "language" not in locale_prediction.keys() or locale_prediction["language"] == "N/A":
            self.language = None
        else:
            self.language = locale_prediction["language"]

        if "country" not in locale_prediction.keys() or locale_prediction["country"] == "N/A":
            self.country = None
        else:
            self.country = locale_prediction["country"]

        if "currency" not in locale_prediction.keys() or locale_prediction["currency"] == "N/A":
            self.currency = None
        else:
            self.currency = locale_prediction["currency"]
