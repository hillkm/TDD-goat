from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_list_and_retrieve_later(self):
        # Alice opens her browser and navigates to the page
        self.browser.get('http://localhost:8000')

        # She reaches the correct homepage
        self.assertIn('To-Do', self.browser.title)
        self.fail('finish the test')

        # It's possible to immediately add to-do items

        # She sets a new task: Investigate JNDI vuln

        # When she hits Enter, the page updates and lists the new task

        # Typing into the text box again, she enters 'Check affected servers'

        # Both items should display properly

        # Text explains that the url for her list is unique and will remember her entries

        # She revisits the list to ensure that is the case

        # Safe knowing her list will be saved for later, she navigates away.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
