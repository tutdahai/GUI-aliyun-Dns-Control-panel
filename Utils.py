from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest

import json




class Utils:
    @staticmethod
    def get_records(accessKeyId,accessSecret,Domain):
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')

        request.set_DomainName(Domain)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        return response
        # print(str(response, encoding='utf-8'))

    @staticmethod
    def get_recordinfo(accessKeyId,accessSecret,recordid):
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = DescribeDomainRecordInfoRequest()
        request.set_accept_format('json')
        
        request.set_RecordId("recordid")

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        return response
        # print(str(response, encoding='utf-8'))
        
    @staticmethod
    def update_mxrecord(accessKeyId,accessSecret,recordid,RR,Type,target,Priority):
        
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(recordid)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(target)
        request.set_Priority(Priority)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        # return response
        # print(str(response, encoding='utf-8'))

    @staticmethod
    def update_record(accessKeyId,accessSecret,recordid,RR,Type,target):
        
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(recordid)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(target)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        # return response
        # print(str(response, encoding='utf-8'))

    @staticmethod
    def add_record(accessKeyId,accessSecret,DomainName,RR,Type,target,Priority):
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_DomainName(DomainName)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(target)
        request.set_Priority(Priority)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        # print(str(response, encoding='utf-8'))

    @staticmethod
    def delete_record(accessKeyId,accessSecret,recordid):
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(recordid)

        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        # print(str(response, encoding='utf-8'))

        
