class EndpointParams(dict):
    """ Crea un diccionario ordinario pero agregando la funcion 'set_params'.
    Ejemplo:
        >>> variable = EndpointParams()
        >>> variable
        {}
        >>> variable.set_params(config, environment)
        >>> variable
        {'algo': 'asignado', 'etc': True, ...}
    """

    def set_params(self, config: dict, environment: str):
        if environment and environment in config:
            self.update(config[environment])
            self['storeId'] = config['storeId']
        elif 'environment' in config and config['environment'] in config:
            self.update(config[config['environment']])
            self['storeId'] = config['storeId']
        else:
            self.update({
                "search_endpoint": config["wcsparams"]["endpoint"],
                "wcs_endpoint": config["wcsparams"]["endpoint_wcs"],
                "storeId": config["wcsparams"]["storeId"]
            })
        self["storeId"] = self["general_store_id"]
