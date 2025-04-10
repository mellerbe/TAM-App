from flask import Flask
from flask import request
from ddtrace import tracer
from random import randint
import logging
from pythonjsonlogger import jsonlogger
import sys

app = Flask(__name__)

# Set up logging to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = jsonlogger.JsonFormatter('%(timestamp)s %(levelname)s %(message)s',)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set global DD tracing
tracer.set_tags({"globalSpanTag": 'backend-301'})

@tracer.wrap(name='generate_dogs', service="listing-dogs", resource='dogs')
def generate_dogs():
    dogcount=randint(1,10)
    logger.info('Generating dogs')
    tracer.current_span().set_tag('count.dogs', dogcount)
    return [
        'Affenpinscher',
        'Afghan Hound',
        'Africanis',
        'Aidi',
        'Airedale Terrier',
        'Akbash',
        'Akita',
        'Aksaray Malaklisi',
        'Alano Español',
        'Alapaha Blue Blood Bulldog',
        'Alaskan husky',
        'Alaskan Klee Kai',
        'Alaskan Malamute',
        'Alopekis'
    ]
@tracer.wrap(name='generate_cats', service="listing-cats", resource='cats')
def generate_cats():
    catcount=randint(1,10)
    logger.warning('Generating cats now')
    tracer.current_span().set_tag('count.cats', catcount)
    return [
        'Abyssinian',
        'Aegean',
        'American Bobtail',
        'American Curl',
        'Americal Shorthair',
        'Maine Coon',
        'RagDoll',
        'Cat'
    ]

# Example custom wrapped function - see https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/
@tracer.wrap(name='custom_resource')
def get_custom_result():
    return f'Custom resource span emitted'


@app.route('/')
def home():
    return 'Welcome to the Animals Info Center!' +\
        '<br>- Use /dogs to get information on dog breeds' +\
        '<br>- Use /cats to get information on cat breeds' +\
        '<br>- Use /custom to see details on request headers' +\
        '<br>- Use /orchestrate to generate traffic'


@app.route('/cats')
def cats():
    return generate_cats()


@app.route('/dogs')
def dogs():
    return generate_dogs()

@app.route('/custom')
def custom():
    return get_custom_result()
    


@app.route('/custom-trace')
def custom_trace():
    return request.headers.get('X-Demo-Header', 'No X-Demo-Header was provided')


@app.route('/debug')
def debug():
    logger.info('Debug endpoint was reached')
    return request.headers.get('X-Demo-Header', 'No X-Demo-Header was provided')


@app.route('/error')
def error():
    logger.error('Debug endpoint was reached')
    raise Exception('Intentional error thrown')


@app.route('/orchestrate')
def generate_traffic():
    for x in range(10):
        generate_dogs()
        generate_cats()
    return 'Traffic has been generated'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)