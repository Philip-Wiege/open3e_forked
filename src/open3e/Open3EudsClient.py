from udsoncan import  services
from udsoncan.common.dids import DataIdentifier

from udsoncan.exceptions import *
from typing import Optional, Any

from udsoncan.client import Client

from open3e.Open3EudsService77 import WriteDataByIdentifier77

class Open3EudsClient(Client):

    def write_data_by_identifier(self, did: int, value: Any, useService77=False) -> Optional[services.WriteDataByIdentifier.InterpretedResponse]:
        """
        Requests to write a value associated with a data identifier (DID) through the :ref:`WriteDataByIdentifier<WriteDataByIdentifier>` service.

        :Effective configuration:  ``exception_on_<type>_response`` ``data_identifiers``

        :param did: The DID to write its value
        :type did: int

        :param value: Value given to the :ref:`DidCodec <DidCodec>`.encode method. The payload returned by the codec will be sent to the server.
        :type value: int

        :return: The server response parsed by :meth:`WriteDataByIdentifier.interpret_response<udsoncan.services.WriteDataByIdentifier.interpret_response>`
        :rtype: :ref:`Response<Response>`

        """
        if not useService77:
            print('Use standard writeDataByIdentifier service 2E ...')
            return super().write_data_by_identifier(did, value)
        else:
            print('Use writeDataByIdentifier service 77 ...')
            req = WriteDataByIdentifier77.make_request(did, value, didconfig=self.config['data_identifiers'])
            self.logger.info("%s - Writing data identifier 0x%04x (%s)" %
                            (self.service_log_prefix(services.WriteDataByIdentifier), did, DataIdentifier.name_from_id(did)))

            response = self.send_request(req)
            if response is None:
                return None
            response = WriteDataByIdentifier77.interpret_response(response)

            if response.service_data.did_echo != did:
                raise UnexpectedResponseException(
                    response, "Server returned a response for data identifier 0x%04x while client requested for did 0x%04x" % (response.service_data.did_echo, did))

            return response
