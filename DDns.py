from Utils import Utils
import json
import os

class DDns:
    @staticmethod
    def save_records(accessKeyId,accessSecret,domain):
        response = str(Utils.get_records(accessKeyId,accessSecret,domain))[2:-1]
        jsonfile = json.loads(response)
        # print(jsonfile)
        with open('records.json','w') as recordsfile:
            json.dump(jsonfile, recordsfile, sort_keys=True, indent=4, separators=(',', ': '))  

    @staticmethod
    def add_record(accessKeyId,accessSecret,DomainName,record_RR,record_type,target):
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
        flag = 0
        for record in records:
            if record["RR"] == record_RR:
                if record["Type"] == record_type:
                    return "already"
                else:
                    continue
            else:
                continue
        Utils.add_record(accessKeyId,accessSecret,DomainName,record_RR,record_type,target)
        return "victory"
                  
    @staticmethod
    def add_mxrecord(accessKeyId,accessSecret,DomainName,record_RR,record_type,target,priority):
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
        flag = 0
        for record in records:
            if record["RR"] == record_RR:
                if record["Type"] == record_type:
                    return "already"
                else:
                    continue
            else:
                continue
        Utils.add_record(accessKeyId,accessSecret,DomainName,record_RR,record_type,target,priority)
        return "victory"

    @staticmethod
    def update_mxrecord(accessKeyId,accessSecret,record_RR,record_type,target,priority):
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
        flag = 0
        for record in records:
            if record["RR"] == record_RR and record["Type"] == record_type:
                if record["Value"] != target:
                    recordid = record["RecordId"]
                    Utils.update_mxrecord(accessKeyId,accessSecret,recordid,record_RR,record_type,target,priority)
                    return "victory"
                elif "Priority" in record:
                    if record['Priority'] != priority:
                        recordid = record["RecordId"]
                        Utils.update_mxrecord(accessKeyId,accessSecret,recordid,record_RR,record_type,target,priority)
                        return "victory"
                else:
                    return "already"
            else:
                continue
        if flag == 0 :
            return "fail"

    @staticmethod
    def update_record(accessKeyId,accessSecret,record_RR,record_type,target):
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
        flag = 0
        for record in records:
            if record["RR"] == record_RR and record["Type"] == record_type:
                if record["Value"] != target:
                    recordid = record["RecordId"]
                    Utils.update_record(accessKeyId,accessSecret,recordid,record_RR,record_type,target)
                    return "victory"
                else:
                    return "already"
            else:
                continue
        if flag == 0 :
            return "fail"

    @staticmethod
    def delete_record(accessKeyId,accessSecret,recordid):
        with open('records.json','r') as recordsfile:
            jsonfile = json.load(recordsfile)
            records = jsonfile["DomainRecords"]["Record"]
        for record in records:
            if record['RecordId'] == recordid:
                Utils.delete_record(accessKeyId,accessSecret,recordid)
                return "victory"
            else:
                continue
        return "fail"
    
    @staticmethod
    def show_records():
        with open('records.json','r') as recordsfile:
            print(recordsfile)