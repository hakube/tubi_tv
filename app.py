from flask import Flask, request
import requests
import datetime


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'

@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    category_slug = request.args.get('slug')
    url = 'https://tubitv.com/oz/containers/{}/content?limit=1000'.format(category_slug)
    
    d = datetime.datetime.today()

    params = dict(method='GET')

    resp = requests.get(url=url, params=params)
    data = resp.json()
    keyfile = None
    harvest = ""
    for i in data:
        keyfile = data['contents'].keys()
    for j in keyfile:
        try:
            duration = data['contents'][j]['duration']
        except KeyError:
            data['contents'][j]['duration'] = 0
        print('{}.{}.{} | {} ({}) | {} | {} | {}\n'.format(d.year, d.month, d.day, data['contents'][j]['title'], data['contents'][j]['year'], datetime.timedelta(seconds=data['contents'][j]['duration']), str(tuple(data['contents'][j]['tags'])).replace('(', '').replace(')', ''), data['contents'][j]['ratings'][0]['value']), end="\n")
        harvest += '{}.{}.{} | {} ({}) | {} | {} | {}<br>'.format(d.year, d.month, d.day, data['contents'][j]['title'], data['contents'][j]['year'], datetime.timedelta(seconds=data['contents'][j]['duration']), str(tuple(data['contents'][j]['tags'])).replace('(', '').replace(')', ''), data['contents'][j]['ratings'][0]['value'])
    harvest += '<script>alert("Batch Completed")</script>'
    
    return harvest

if __name__ == '__main__':
    app.run()