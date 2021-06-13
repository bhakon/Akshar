import json
import nlpcloud
import requests

main_part = "api_ZzORHqQQAGyPQmRYrRkqcWfSqGkgSMpUKc"
token = "Bearer " + main_part

'''
def question_answering(question, context):
    headers = {"Authorization": token}
    API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    data = query(
        {
            "inputs": {
                "question": question,
                "context": context,
            }
        }
    )

    return data['answer']

'''
def at_sum(context):
    client = nlpcloud.Client("bart-large-cnn", "dadbdbaebb34b57763094752c9049a932a725028")
    result = client.summarization(context)
    return result['summary_text']

def translate_text_hi_en(input_text):
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-hi-en"
    headers = {"Authorization": token}

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    data = query(
        {
            "inputs": input_text,
        }
    )
    return data[0]['translation_text']


def translate_text_en_hi(input_text):
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi"
    headers = {"Authorization": token}

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    data = query(
        {
            "inputs": input_text,
        }
    )
    return data[0]['translation_text']





def title_gen(context):
    API_URL = "https://api-inference.huggingface.co/models/Callidior/bert2bert-base-arxiv-titlegen"
    headers = {"Authorization": token}

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    data = query(
        {
            "inputs": context,
        }
    )
    return data[0]['summary_text']




def question_answering(question, context):
    client = nlpcloud.Client("roberta-base-squad2", "dadbdbaebb34b57763094752c9049a932a725028")
    print("fine 1 -----------------")
    print(context )
    print("----------------------------")
    print(question , "--------------------")
    result = client.question(context, question)
    print("fine 2 ---------------")
    return result['answer']

def at_sum(context):
    headers = {"Authorization": token}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    data = query(
        {
            "inputs": context,
        }
    )

    return data[0]['summary_text']

