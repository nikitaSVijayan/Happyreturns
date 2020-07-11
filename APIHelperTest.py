import json
import requests


class APIHelperException(Exception):
    pass


class APIHelper:

    def __init__(self):
        # Get the product variant from the api endpoint
        output = self.getProductVariant(url='https://happyreturnsqatest.free.beeceptor.com/getProductVariants')
        # Get a variant object from the array variants
        variant_obj = output.get('variants')[0]
        # Post the data
        self.postOrder(url='https://happyreturnsqatest.free.beeceptor.com/order', payloadData=variant_obj)

    def _errorCode(self, response, url):
        """ Process error code"""
        statusCode = response.status_code
        errorStr = None
        if response.status_code >= 500:
            print '[{}] Server Error: {}'.format(response.status_code, url)
        elif statusCode == 404:
            errorStr = '[{}] URL not found: {}'.format(statusCode, url)
        elif statusCode == 403:
            errorStr = '[{}] Forbidden - user does not have the necessary permissions for the resource {}'.format(
                statusCode, url)
        elif statusCode == 401:
            errorStr = '[{}] Authentication Failed'.format(statusCode)
        elif statusCode == 400:
            errorStr = '[{}] Bad Request'.format(statusCode)
        else:
            errorStr = 'Unexpected Error: [HTTP {}]: Content: {}'.format(statusCode, response.content)
        raise APIHelperException(errorStr)

    def _getRequest(self, url):
        """
        Gets the data from the end point
        :return: Dict: Response text
        """
        response = requests.get(url)
        if response.status_code != 200:
            self._errorCode(response, url)
        else:
            print 'Successfully received response {} from {}'.format(response.content, url)
            return json.loads(response.text)

    def _postRequest(self, url, payload):
        """
        Sends a post request to an end point
        :return: response
        """
        response = requests.post(url, json=payload)
        return response

    def getProductVariant(self, url):
        """
        Get the product variant details from the given endpoint
        :param url: Endpoint
        :return: reponse
        """
        response = self._getRequest(url)
        return response

    def postOrder(self, url, payloadData):
        """
        Update the existing values with payload data
        :param payloadData: (Dict) Data to be sent to the api
        :return: response
        """
        if not payloadData:
            errorStr = "Invalid payload {}".format(payloadData)
            raise APIHelperException(errorStr)
        payload = {'variants': payloadData}
        print payload
        response = self._postRequest(url, json.dumps(payload))
        return response

APIHelper = APIHelper()
