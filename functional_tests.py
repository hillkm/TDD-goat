from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # It's possible to immediately add to-do items
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                "Enter a to-do task"
        )

        # She sets a new task: Investigate JNDI vuln
        inputbox.send_keys('Investigate JNDI injection')

        # When she hits Enter, the page updates and lists the new task
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Investigate JNDI injection' for row in rows),
                "New row does not appear in table"
        )

        # Typing into the text box again, she enters 'Check affected servers'
        self.fail('Finish the test')

        # Both items should display properly

        # Text explains that the url for her list is unique and will remember her entries

        # She revisits the list to ensure that is the case

        # Safe knowing her list will be saved for later, she navigates away.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
