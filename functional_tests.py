from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_get_calendar_of_popular_events(self):
        # Kevin hears about a faster way to find popular Meetup.com events. He
        # doesn't like having to mentally keep track of events sorted by time to
        # figure out which ones are the most popular for that day.
        # he goes to thepopularevents.com
        self.browser.get('http://django.dev:8000')

        # He notices that the page mentions The Popular Events
        self.assertIn('The Popular Events', self.browser.title)
        self.fail('Finish the test!')

        # A calendar, that starts that day, with up to 3 most popular events per
        # day is shown. An input box for city is filled in. The dropdown for
        # miles radius is set to 25 miles. The input box for search is empty.
        # There will be a list of categories one can click.



if __name__ == '__main__':
    unittest.main(warnings='ignore')
