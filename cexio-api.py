#!/usr/bin/python

import hmac, hashlib
import requests
import json
import time
import sys

class API(object):
  def __init__(self, user_id, api_key, api_secret):
    self.user_id = user_id
    self.api_key = api_key
    self.api_secret = api_secret

  def set_nonce(self):
    self.nonce = '{:.10f}'.format(time.time() * 1000).split('.')[0]

  def get_signature(self):
    self.set_nonce()
    message = self.nonce + self.user_id + self.api_key
    return hmac.new(self.api_secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

  def get_params(self):
    params = dict(
      key = self.api_key,
      signature = self.get_signature(),
      nonce = self.nonce
    )
    return params

  def request_url(self, url, params):
    r = requests.post(url=url, data=params)
    data = json.loads(r.text)
    return data

  def api_call(self, api_function, private=False, pair=''):
    url = 'https://cex.io/api/' + api_function + '/' + pair
    if private:
      params = self.get_params()
    else:
      params = {}
    return self.request_url(url, params)

  def balance(self):
    return self.api_call('balance', True)

  def archived_orders(self, pair):
    return self.api_call('archived_orders', True, pair)

  def open_orders(self):
    return self.api_call('open_orders', True)

  def last_price(self, pair):
    return self.api_call('last_price', False, pair)
