class TextExtractor:

    @staticmethod
    def split_segments(text):

        separators = (

            ".",
            ";",
            "!",
            "?",
            "\n"

        )

        for separator in separators:

            text = text.replace(separator, "|")

        segments = text.split("|")

        cleaned_segments = []

        for segment in segments:

            segment = segment.strip()

            if segment:

                cleaned_segments.append(segment)

        return cleaned_segments

    @staticmethod
    def split_items(text):

        separators = (

            ",",
            ";",
            " y ",
            " e "

        )

        for separator in separators:

            text = text.replace(separator, "|")

        preferences = text.split("|")

        cleaned_preferences = []

        for preference in preferences:

            preference = preference.strip()

            preference = TextExtractor.remove_initial_modifier(preference)

            preference = TextExtractor.remove_initial_article(preference)

            preference = TextExtractor.remove_trailing_punctuation(preference)

            if preference:

                cleaned_preferences.append(preference)

        return cleaned_preferences

    @staticmethod
    def remove_initial_article(text):

        articles = (

            "el ",
            "la ",
            "los ",
            "las ",
            "un ",
            "una ",
            "unos ",
            "unas "

        )

        for article in articles:

            if text.startswith(article):

                return text[len(article):]

        return text

    @staticmethod
    def remove_initial_modifier(text):

        modifiers = (

            "muchísimo ",
            "muchísima ",
            "muchísimos ",
            "muchísimas ",

            "bastante ",
            "bastantes ",

            "realmente ",
            "verdaderamente ",
            "especialmente ",

            "demasiado ",
            "demasiada ",
            "demasiados ",
            "demasiadas "

        )

        for modifier in modifiers:

            if text.startswith(modifier):

                return text[len(modifier):]

        return text

    @staticmethod
    def remove_trailing_punctuation(text):

        punctuation = ".,;:!?¡¿"

        return text.rstrip(punctuation)