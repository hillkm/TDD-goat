from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_start_list_and_retrieve_later(self):
        # Alice opens her browser and navigates to the page
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1: Investigate JNDI injection')

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Investigate JNDI injection')

        # Typing into the text box again, she enters 'Check affected servers'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Check affected servers')
        inputbox.send_keys(Keys.ENTER)

        # Both items should display properly
        self.wait_for_row_in_list_table('1: Investigate JNDI injection')
        self.wait_for_row_in_list_table('2: Check affected servers')

        # Text explains that the url for her list is unique and will remember her entries
        
        # She revisits the list to ensure that is the case

        # Safe knowing her list will be saved for later, she navigates away.

    def test_multi_users_can_start_lists_at_diff_urls(self):
        # Eve starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Investigate JNDI injection')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Investigate JNDI injection')

        # She's saving her list at a unique URL
        eve_list_url = self.browser.current_url
        self.assertRegex(eve_list_url, '/lists/.+')

        # Bob tries to use the site
        ## Using a new session to prevent possible failures from cache/cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Investigate JNDI injection', page_text)
        self.assertNotIn('Check affected servers', page_text)

        # Bob starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Setup dev environment')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Setup dev environment')

        # Bob's URL is different from other users
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, eve_list_url)

        # Bob cannot see Eve's list, but can see his own entries
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Investigate JNDI injection')
        self.assertIn('Setup dev environment')

        # both users navigate away from the page
