from flask import Flask, jsonify
import redis

r = redis.Redis(host='redis', port=6379)
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Type a number in the browser where number is K in Fibonacci'


def fibonacci(number):
    if (number == 0) or (number == 1):
        return number
    return fibonacci(number - 1) + fibonacci(number - 2)


@app.route("/<number>", methods=['GET'])
def get_fibonacci_api(number):
    number = int(number)
    print(number)
    cached_data = r.get(number)
    if cached_data:
        return jsonify({number: cached_data.decode()}), 200
    new_data = fibonacci(number)
    r.set(number, new_data)
    return jsonify({number: new_data}), 200
