##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2019, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import os
import time

from selenium.webdriver import ActionChains
from regression.python_test_utils import test_utils
from regression.feature_utils.base_feature_test import BaseFeatureTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .locators import QueryToolLocatorsCss

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

config_data = config_data_json = {}
# try:
with open(CURRENT_PATH + '/test_data.json') as data_file:
    config_data_json = json.load(data_file)
# except Exception as e:
#     print(str(e))


class CheckForViewDataTest(BaseFeatureTest):
    """
    Test cases to validate insert, update operations in table
    with input test data

    First of all, the test data is inserted/updated into table and then
    inserted data is compared with original data to check if expected data
    is returned from table or not.

    We will cover test cases for,
        1) Insert with default values
        2) Update with null values
        3) Update with blank string
        4) Copy/Paste row
    """

    scenarios = [
        ("Validate Insert, Update operations in View/Edit data with "
         "given test data",
         dict())
    ]

    TIMEOUT_STRING = "Timed out waiting for div element to appear"

    # query for creating 'defaults_text' table
    defaults_query = """
CREATE TABLE public.defaults_{0}
(
    {1} serial NOT NULL,
    number_defaults numeric(100) DEFAULT 1,
    number_null numeric(100),
    text_defaults text COLLATE pg_catalog."default"
        DEFAULT 'Hello World'::text,
    text_null1 text COLLATE pg_catalog."default",
    text_null2 text COLLATE pg_catalog."default",
    text_null3 text COLLATE pg_catalog."default",
    text_null4 text COLLATE pg_catalog."default",
    json_defaults json DEFAULT '[51, 52]'::json,
    json_null json,
    boolean_true boolean DEFAULT true,
    boolean_null boolean,
    boolean_false boolean,
    text_arr text[],
    text_arr_empty text[],
    text_arr_null text[],
    int_arr integer[],
    int_arr_empty integer[],
    boolean_arr boolean[],
    boolean_arr_null boolean[],
    CONSTRAINT defaults_pkey_{0} PRIMARY KEY ({1})
)
"""
    non_int_pkey_table = """
CREATE TABLE public.nonintpkey
(
    charid text COLLATE pg_catalog."default" NOT NULL,
    col1 text,
    col2 numeric(100),
    CONSTRAINT nonintpkey_pkey PRIMARY KEY (charid)
)
    """

    def before(self):
        with test_utils.Database(self.server) as (connection, _):
            if connection.server_version < 90100:
                self.skipTest(
                    "COLLATE is not present in PG versions below v9.1"
                )

        # Create pre-requisite table
        for k, v in {1: 'id', 2: '"ID"'}.items():
            test_utils.create_table_with_query(
                self.server,
                self.test_db,
                CheckForViewDataTest.defaults_query.format(k, v))

        test_utils.create_table_with_query(
            self.server,
            self.test_db,
            CheckForViewDataTest.non_int_pkey_table
        )

        # Initialize an instance of WebDriverWait with timeout of 3 seconds
        self.wait = WebDriverWait(self.driver, 3)

        # close the db connection
        connection.close()

    def runTest(self):
        self.page.wait_for_spinner_to_disappear()
        self.page.add_server(self.server)
        self._tables_node_expandable()

        self._load_config_data('table_insert_update_cases')
        # iterate on both tables
        for cnt in (1, 2):
            self._perform_test_for_table('defaults_{0}'.format(str(cnt)))

        # test nonint pkey table
        self._load_config_data('table_insert_update_nonint')
        self._perform_test_for_table('nonintpkey')

    def after(self):
        self.page.remove_server(self.server)

    @staticmethod
    def _get_cell_xpath(cell, row):

        if row == 1:
            xpath_grid_row = "//*[contains(@class, 'ui-widget-content') " \
                             "and contains(@style, 'top:0px')]"
        else:
            xpath_grid_row = "//*[contains(@class, 'ui-widget-content') " \
                             "and contains(@style, 'top:25px')]"

        xpath_row_cell = '//div[contains(@class, "' + cell + '")]'

        xpath_cell = '{0}{1}'.format(xpath_grid_row, xpath_row_cell)

        return xpath_cell

    @staticmethod
    def _load_config_data(config_key):
        global config_data
        config_data = config_data_json[config_key]

    def _perform_test_for_table(self, table_name):
        self.page.select_tree_item(table_name)
        # Open Object -> View/Edit data
        self._view_data_grid(table_name)

        self.page.wait_for_query_tool_loading_indicator_to_disappear()
        # Run test to insert a new row in table with default values
        self._add_row()
        self._verify_row_data(True, config_data['add'])

        # Run test to copy/paste a row
        self._copy_paste_row()

        self._update_row()
        self.page.click_tab("Messages")
        self._verify_messsages("")
        self.page.click_tab("Data Output")
        updated_row_data = {
            i: config_data['update'][i] if i in config_data['update'] else val
            for i, val in config_data['add'].items()
        }
        self._verify_row_data(False, updated_row_data)

        self.page.close_data_grid()

    def _compare_cell_value(self, xpath, value):
        # Initialize an instance of WebDriverWait with timeout of 5 seconds
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, xpath + "//span"), str(value)),
                CheckForViewDataTest.TIMEOUT_STRING
            )
        except Exception:
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, xpath), str(value)),
                CheckForViewDataTest.TIMEOUT_STRING
            )

    def _update_cell(self, xpath, data):
        """
        This function updates the given cell(xpath) with
        given value
        Args:
            xpath: xpath of cell element
            data: list with cell related data

        Returns: None

        """

        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, xpath)), CheckForViewDataTest.TIMEOUT_STRING
        )
        cell_el = self.page.find_by_xpath(xpath)
        self.page.driver.execute_script("arguments[0].scrollIntoView(false)",
                                        cell_el)
        ActionChains(self.driver).move_to_element(cell_el).double_click(
            cell_el
        ).perform()
        cell_type = data[2]
        value = data[0]

        if cell_type in ['int', 'int[]']:
            if value == 'clear':
                cell_el.find_element_by_css_selector('input').clear()
            else:
                ActionChains(self.driver).send_keys(value).\
                    send_keys(Keys.ENTER).perform()
        elif cell_type in ['text', 'json', 'text[]', 'boolean[]']:
            text_area_ele = self.page.find_by_css_selector(
                ".pg-text-editor > textarea")
            text_area_ele.clear()
            text_area_ele.click()
            text_area_ele.send_keys(value)

            # Click on editor's Save button
            self.page.find_by_css_selector(
                '.btn.btn-primary.long_text_editor').click()
        else:
            # Boolean editor test for to True click
            if data[1] == 'true':
                checkbox_el = cell_el.find_element_by_xpath(
                    ".//*[contains(@class, 'multi-checkbox')]")
                checkbox_el.click()
            # Boolean editor test for to False click
            elif data[1] == 'false':
                checkbox_el = cell_el.find_element_by_xpath(
                    ".//*[contains(@class, 'multi-checkbox')]")
                # Sets true
                checkbox_el.click()
                # Sets false
                ActionChains(self.driver).click(checkbox_el).perform()

    def _tables_node_expandable(self):
        self.page.toggle_open_tree_item(self.server['name'])
        self.page.toggle_open_tree_item('Databases')
        self.page.toggle_open_tree_item(self.test_db)
        self.page.toggle_open_tree_item('Schemas')
        self.page.toggle_open_tree_item('public')
        self.page.toggle_open_tree_item('Tables')

    def _view_data_grid(self, table_name):
        self.page.driver.find_element_by_link_text("Object").click()
        ActionChains(
            self.page.driver
        ).move_to_element(
            self.page.driver.find_element_by_link_text("View/Edit Data")
        ).perform()
        self.page.find_by_partial_link_text("All Rows").click()
        time.sleep(1)
        # wait until datagrid frame is loaded.

        self.page.click_tab(table_name)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'iframe')
            ), CheckForViewDataTest.TIMEOUT_STRING
        )
        self.page.driver.switch_to.frame(
            self.page.driver.find_element_by_tag_name('iframe')
        )

    def _copy_paste_row(self):
        row0_cell0_xpath = CheckForViewDataTest._get_cell_xpath("r0", 1)

        self.page.find_by_xpath(row0_cell0_xpath).click()
        self.page.find_by_xpath("//*[@id='btn-copy-row']").click()
        self.page.find_by_xpath("//*[@id='btn-paste-row']").click()

        # Update primary key of copied cell
        self._add_update_save_row(config_data['copy'], row=2)

        # Verify row 1 and row 2 data
        updated_row_data = {
            i: config_data['copy'][i] if i in config_data['copy'] else val
            for i, val in config_data['add'].items()
        }
        self._verify_row_data(False, updated_row_data)

    def _add_update_save_row(self, data, row=1):
        for idx in data.keys():
            cell_xpath = CheckForViewDataTest._get_cell_xpath(
                'r' + str(idx), row
            )
            time.sleep(0.2)
            self._update_cell(cell_xpath, data[str(idx)])
        self.page.find_by_id("btn-save-data").click()  # Save data
        # There should be some delay after save button is clicked, as it
        # takes some time to complete save ajax call otherwise discard unsaved
        # changes dialog will appear if we try to execute query before previous
        # save ajax is completed.
        time.sleep(2)

    def _add_row(self):
        self._add_update_save_row(config_data['add'], 1)

    def _update_row(self):
        self._add_update_save_row(config_data['update'], 1)

    def _verify_messsages(self, text):
        messages_ele = self.page.find_by_css_selector(
            QueryToolLocatorsCss.query_messages_panel)
        self.assertEquals(text, messages_ele.text)

    def _verify_row_data(self, is_new_row, config_check_data):
        self.page.find_by_id("btn-flash").click()

        # First row if row height = 0, second row if its 25
        row_height = 0 if is_new_row else 25

        xpath = "//*[contains(@class, 'ui-widget-content') and " \
                "contains(@style, 'top:" + str(row_height) + "px')]"

        self.page.wait_for_query_tool_loading_indicator_to_disappear()

        result_row = self.page.find_by_xpath(xpath)

        # List of row values in an array
        for idx in config_check_data.keys():
            element = result_row.find_element_by_class_name("r" + str(idx))
            self.page.driver.execute_script(
                "arguments[0].scrollIntoView(false)", element)

            self.assertEquals(element.text, config_check_data[str(idx)][1])
            self.assertEquals(element.text, config_check_data[str(idx)][1])

        # scroll browser back to the left
        # to reset position so other assertions can succeed
        for idx in reversed(list(config_check_data.keys())):
            element = result_row.find_element_by_class_name("r" + str(idx))
            self.page.driver.execute_script(
                "arguments[0].scrollIntoView(false)", element)
