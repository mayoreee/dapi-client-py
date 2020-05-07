import grpc

import rpc.grpc.core_pb2 as core_pb2
import rpc.grpc.core_pb2_grpc as core_pb2_grpc
import rpc.grpc.platform_pb2 as platform_pb2
import rpc.grpc.platform_pb2_grpc as platform_pb2_grpc
#import platform_resources

import cbor2
import base64

GRPC_REQUEST_TIMEOUT = 5

# Set up connection
channel = grpc.insecure_channel('evonet.thephez.com:3010')
stub = platform_pb2_grpc.PlatformStub(channel)
stubCore = core_pb2_grpc.CoreStub(channel)


def get_identity(id):
    # Get Identity
    #identity_id = 'Bb2p582MFR1tQhVQHKrScsAJH6Erqsb6SoroD9dQhJ5e'
    # Create Identity request
    get_identity_request = platform_pb2.GetIdentityRequest()
    # Set identity parameter of request
    get_identity_request.id = id

    #get_identity_response = platform_pb2.GetIdentityResponse()
    get_identity_response = stub.getIdentity(get_identity_request, GRPC_REQUEST_TIMEOUT)
    #print(get_identity_response)
    print('Identity Response: {}\n'.format(cbor2.loads(get_identity_response.identity)))

    #print(dir(identity_response))

def get_data_contract(contract_id):
    # Get Data Contract
    #dpns_contract_id = '2KfMcMxktKimJxAZUeZwYkFUsEcAZhDKEpQs8GMnpUse'
    contract_request = platform_pb2.GetDataContractRequest()
    contract_request.id = contract_id

    data_contract = stub.getDataContract(contract_request, GRPC_REQUEST_TIMEOUT)
    print(data_contract)
    print('Data Contract: {}\n'.format(cbor2.loads(data_contract.data_contract)))

def get_documents(contract_id, type, options):
    # Get Document
    #contract_id = dpns_contract_id

    document_request = platform_pb2.GetDocumentsRequest()
    document_request.data_contract_id = contract_id
    document_request.document_type =  type
    document_request.limit =  2
    #document_request.where = # Requires cbor (found in dapi-client)

    docs = stub.getDocuments(document_request, GRPC_REQUEST_TIMEOUT)
    #print(docs)
    for d in docs.documents:
        print('Document cbor: {}\n'.format(cbor2.loads(d)))

def get_block(height):
    # Get Block
    block_request = core_pb2.GetBlockRequest()
    block_request.height = height

    block_response = stubCore.getBlock(block_request, GRPC_REQUEST_TIMEOUT)
    print('Block: {}\n'.format(block_response.block))

def get_status():
    status_request = core_pb2.GetStatusRequest()

    status_response = stubCore.getStatus(status_request, GRPC_REQUEST_TIMEOUT)
    print('Status: {}\n'.format(status_response))

def get_transaction(id):
    transaction_request = core_pb2.GetTransactionRequest()
    transaction_request.id = id

    transaction_response = stubCore.getTransaction(transaction_request, GRPC_REQUEST_TIMEOUT)
    print('Transaction: {}\n'.format(transaction_response.transaction))

def main():
    identity_id = 'JCaTiRxm4dRN1GJqoNkpowmvisC7BbgPW48pJ6roLSgw'
    dpns_contract_id = '5wpZAEWndYcTeuwZpkmSa8s49cHXU5q2DhdibesxFSu8'
    transaction_id = '29b68163a22d89c14e24f1281cb4608b8dc7be05bc2604e2cecf8a85b1dede0d'

    get_identity(identity_id)
    get_data_contract(dpns_contract_id)
    get_documents(dpns_contract_id, 'note', 'limit = 2')
    get_block(1)
    get_status()
    get_transaction(transaction_id)

if __name__ == "__main__":
    main()
