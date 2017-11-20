from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://django.dev:8000/')

assert 'Django' in browser.title
