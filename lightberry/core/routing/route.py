from lightberry.utils import requests_utils


class Route:
    def __init__(self, url, handler, methods):
        self.methods = methods if methods else ["GET"]

        self.url = url
        self.url_data = []
        self.accepts_path_params = False

        self.handler = handler

        self.__parse_url()

    def __parse_url(self):
        data = []
        split_url = self.url.split("/")

        for index, segment in enumerate(split_url):
            is_parameter = segment.startswith(":")

            if is_parameter and not self.accepts_path_params:
                self.accepts_path_params = True

            data.append({
                "position": index,
                "content": segment,
                "is_parameter": is_parameter,
                "parameter_name": segment[1::] if is_parameter else None
            })

        self.url_data = data

    def get_path_parameters_for_url(self, url):
        parameters = {}
        split_url = url.split("/")

        for data_part in self.url_data:
            if data_part["is_parameter"]:
                parameters[data_part["parameter_name"]] = split_url[data_part["position"]]

        return parameters

    def match_url(self, url):
        split_test_url = url.split("?")[0].split("/")

        lengths_match = True if len(split_test_url) == len(self.url_data) else False
        pattern_match = True

        if lengths_match:
            for index, data_segment in enumerate(self.url_data):
                split_test_url_part = split_test_url[index]

                if (split_test_url_part != data_segment["content"]) and not data_segment["is_parameter"]:
                    pattern_match = False
                    break

        return True if (lengths_match and pattern_match) else False

    def concat_url_with_parameters(self, path_parameters, query_params):
        url = self.url

        if path_parameters:
            for parameter in path_parameters:
                parameter_value = path_parameters.get(parameter)
                parameter_value = str(parameter_value) if parameter_value else parameter_value

                url = url.replace(f":{parameter}", parameter_value)

        url = requests_utils.add_query_params_to_url(url, query_params)
        url = requests_utils.url_encode(url)

        return url
