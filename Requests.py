import urllib3



class Requests():
    """Singleton for sening HTTP requests
    """


    __instance = None # Singeton instance


    def instance():
        """Returns instance of this singleton

        Returns:
            Requests: Requests object instance
        """
        if Requests.__instance is None:
            Requests.__instance = Requests()
            Requests.__instance.__create()
        return Requests.__instance
    

    def __create(cls):
        """Creating pool manager
        """
        cls.http = urllib3.PoolManager()


    def request(cls, address: str):
        """Creating a HTTP requests

        Args:
            address (str): URL

        Returns:
            urllib3.response.HTTPResponse: Response result
        """
        return cls.http.request('GET', address, headers={'Accept': 'application/json'}, timeout=urllib3.util.Timeout(2))