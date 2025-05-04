from pathlib import Path
from python_selenium.rest.rest_configuration import RestConfiguration


class SwaggerPetstoreConfiguration(RestConfiguration):

    def __init__(
            self,
            path: Path = Path("resources/swagger-petstore-default-config.ini")):
        super().__init__(path)
