from flask_socketio import Namespace, emit
from .utils import log_event, retrieve_log_queue
from flask import render_template


class LogsNamespace(Namespace):
    def on_log_event(self, data):
        status, message = log_event(data.get('userId'), data.get('password'), data.get('type'), data.get('location'), data.get('context'))
        # message = encrypt_data(json.dumps(message))
        if status:
            emit('return_log_event', message)
        else:
            emit('error_log_event', message)
    
    def on_retrieve_new_logs(self, data):
        status, message = retrieve_log_queue(data.get('userId'), data.get('password'))

class DataLayer:
    def __init__(self,username,password):
        self._username = username
        self._password = password

        result = retrieve_log_queue(username,password)
        #print(result)
        ordered_Dict = 0
        def return_Ordered_Dict(input_tuple):
            if isinstance(input_tuple, tuple) and len(input_tuple) == 2:
                ordered_dict = input_tuple[1]
                return ordered_dict


        final_order_dict = return_Ordered_Dict(result)
        #print(final_order_dict)
        def return_record(ordered_dict):
            list_of_dictionaries = []
            for record in final_order_dict:
                #print(final_order_dict[record])
                list_of_dictionaries.append(final_order_dict[record])
            return list_of_dictionaries

        self._list_of_dict = return_record(final_order_dict)
        #print(self._list_of_dict)
    
    @staticmethod
    def Render_List_Of_Dict_To_Html(dictlist,full_url):
        colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

        labels = []
        values = []
        result = {}
        for dict in dictlist:
            key = dict['type of offense'] # type of offense, Breach of Security Policy

            if key in result:
                result[key] = result[key] + 1
            else:
                result[key] = 1

        print(result)

        for key in result:
            labels.append(key)
            values.append(result[key])

        print(labels)
        print(values)

        # return render_template("Logs.html",list_of_dict = datalayer._list_of_dict)
        return render_template("Logs.html",
                            list_of_dict = dictlist,
                            max = 17000,
                            set = zip(values, labels, colors),full_url = full_url)