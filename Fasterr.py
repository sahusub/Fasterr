import xlrd
import datetime
import collections
import selenium
from selenium import webdriver, common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
import xlrd
import unittest
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option('useAutomationExtension', False)

capabilities = { 'chrome_options':  { 'useAutomationExtension': False,
                                     'args': ['--disable-extensions'] }
               }
global driver
driver = webdriver.Chrome(
    r'C:\Users\sahusub\Downloads\chromedriver_win32\chromedriver.exe', desired_capabilities = capabilities, options=chrome_options)

driver.set_window_size(1024, 600)
driver.maximize_window()
chrome_options.add_argument('disable-extensions')
chrome_options.add_argument('disable-infobars')


def loginForDEVQA():

    driver.get('https://novartis3-sb.pvcloud.com/testing/')

    DSN = Select(driver.find_element_by_name('DSN'))
    DSN.select_by_visible_text('NVTSB1DEV')
    username = driver.find_element_by_id('Username')
    password = driver.find_element_by_id('UserPass')
    username.send_keys('sahusub')
    password.send_keys('horizon')
    password.submit()
    print('Login is done !!')


def login():
    driver.get('https://novartis.pvcloud.com/planview/')
    print('Login tp PROD PV is done !!')


def openWP(wpcode):
    print('Opening WP: ', wpcode)
    searchbox = driver.find_element_by_id('bannerSearchBox')
    time.sleep(4)
    searchbox.clear()
    '''
    for i in wpcode:
        searchbox.send_keys(i)
        time.sleep(.5)
    '''
    searchbox.send_keys(wpcode)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    WPCode_in_SearchResult = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="searchResults"]/tbody/tr[2]/td[4]')))
    if WPCode_in_SearchResult.text == wpcode:

        ele1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, r'//*[@class="form-field"]/span/span')))
        ele1.click()
        ele2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, r'//*[@id="pvPopup1pvPopup"]/ul/li[2]')))
        ele2.click()
        time.sleep(20)
        ele3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, r'//*[contains(@id,"text-filter-")]')))
        ele3.send_keys('I11Z Trial Management')
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[contains(@title,": I11Z Trial Management")]').click()

        ActionChains(driver) \
            .key_down(Keys.SHIFT) \
            .key_down(Keys.F9) \
            .key_up(Keys.SHIFT) \
            .key_up(Keys.F9)\
            .perform()

        seq = driver.find_elements_by_tag_name('iframe')
        print(len(seq))

        Reserve = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ui-id-6')))
        Reserve.click()
    else:
        print("WP Code Requested: "+wpcode +
              " But WP Opened: "+WPCode_in_SearchResult.text)
        searchbox = driver.find_element_by_id('bannerSearchBox')
        time.sleep(4)
        searchbox.clear()

        for i in wpcode:
            searchbox.send_keys(i)
            time.sleep(.5)

        # searchbox.send_keys(wpcode)
        time.sleep(5)
        searchbox.send_keys(Keys.ENTER)
        WPCode_in_SearchResult = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
            (By.XPATH, r'//*[@id="searchResults"]/tbody/tr[2]/td[4]')))
        if WPCode_in_SearchResult.text == wpcode:

            ele1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, r'//*[@class="form-field"]/span/span')))
            ele1.click()
            ele2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, r'//*[@id="pvPopup1pvPopup"]/ul/li[2]')))
            ele2.click()
            time.sleep(20)
            ele3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, r'//*[contains(@id,"text-filter-")]')))
            ele3.send_keys('I11Z Trial Management')
            time.sleep(2)
            driver.find_element_by_xpath(
                '//*[contains(@title,": I11Z Trial Management")]').click()

            ActionChains(driver) \
                .key_down(Keys.SHIFT) \
                .key_down(Keys.F9) \
                .key_up(Keys.SHIFT) \
                .key_up(Keys.F9)\
                .perform()

            seq = driver.find_elements_by_tag_name('iframe')
            print(len(seq))

            Reserve = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ui-id-6')))
            Reserve.click()


def addResource(Res):

    NewReserve = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="taskreserve-0-insertButtonContainer"]/span[2]')))
    NewReserve.click()

    time.sleep(2)

    MainWindow = driver.window_handles[0]
    DataPicker = driver.window_handles[1]
    driver.switch_to_window(DataPicker)
    seq = driver.find_elements_by_tag_name('iframe')
    print(len(seq))
    Search = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="pickerTabBar"]/li[2]/a')))
    Search.click()
    time.sleep(3)

    driver.switch_to_frame('iframeSearchView')
    driver.switch_to_frame('frameAttributes')

    SearchDescription = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, 'attribute_description')))
    SearchDescription.send_keys(Res)

    SearchButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, '_search')))
    SearchButton.click()

    driver.switch_to_default_content()
    driver.switch_to_frame('iframeSearchView')
    driver.switch_to_frame('frameSearchList')
    ResourceCheckBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@type="checkbox" and @name="sel_list"]')))
    ResourceCheckBox.click()
    driver.switch_to_default_content()


def addMultResource(Res):
    driver.switch_to_frame('iframeSearchView')
    driver.switch_to_frame('frameAttributes')

    SearchDescription = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, 'attribute_description')))
    SearchDescription.clear()
    SearchDescription.send_keys(Res)
    SearchButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, '_search')))
    SearchButton.click()

    driver.switch_to_default_content()
    driver.switch_to_frame('iframeSearchView')
    driver.switch_to_frame('frameSearchList')
    time.sleep(2)
    ResourceCheckBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@type="checkbox" and @name="sel_list"]')))

    ResourceCheckBox.click()
    driver.switch_to_default_content()


def addUtilization(Res, SDate, EDate, UT, Req):

    time.sleep(4)
    UpBotton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="pv-tabs-1-panel"]/div[2]/div[2]/div[2]/div/div[1]')))
    UpBotton.click()

    #driver.find_element_by_xpath(r'//*[contains(@title, "'+Res+'")]').click()
    time.sleep(2)

    driver.find_element_by_xpath(
        r'//*[@id="taskreserve-0-findFilterContainer"]//input').click()
    driver.find_element_by_xpath(
        r'//*[@id="taskreserve-0-findFilterContainer"]//input').clear()
    driver.find_element_by_xpath(
        r'//*[@id="taskreserve-0-findFilterContainer"]//input').send_keys(Res)
    time.sleep(2)
    driver.find_element_by_xpath(r'//*[contains(@title, "'+Res+'")]').click()
    time.sleep(2)
    
    Utilization = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="taskreserve-0-grid-widget__grid-0"]/div[4]/div[3]/div/div[2]/div[10]/div')))
    Utilization.click()
    actions = ''
    actions = ActionChains(driver)
    time.sleep(1)
    actions.send_keys(Keys.ENTER)
    actions.send_keys('0')
    time.sleep(1)
    actions.perform()
    time.sleep(2)
    '''
# *Start******Adding Role (GTD/GTM)**********************
    if len(driver.find_elements_by_xpath(r'//a[text() = "No Country"]')) > 0:
        driver.find_element_by_xpath(r'//a[text() = "No Country"]').click()
        time.sleep(2)
        MainWindow = driver.window_handles[0]
        DataPicker = driver.window_handles[1]
        driver.switch_to.window(DataPicker)
        time.sleep(2)
        if Req == 'GTD':
            driver.find_element_by_xpath(r'//*[contains(@value, "|1|")]').click()
            driver.find_element_by_id('OK').click()        
        
        elif Req == 'GTM':
            driver.find_element_by_xpath(r'//*[contains(@value, "|2|")]').click()
            driver.find_element_by_id('OK').click()
        elif Req == 'NA':
            driver.find_element_by_xpath(r'//*[contains(@value, "||")]').click()
            driver.find_element_by_id('OK').click()
            
        time.sleep(2)
        driver.switch_to.window(MainWindow)
        
    elif len(driver.find_elements_by_xpath(r'//*[@id="taskreserve-0-grid-widget__grid-0"]/div[4]/div[3]/div/div[2]/div[3]/div/a')) > 0:
        driver.find_element_by_xpath(
            r'//*[@id="taskreserve-0-grid-widget__grid-0"]/div[4]/div[3]/div/div[2]/div[3]/div/a').click()
        time.sleep(2)
        MainWindow = driver.window_handles[0]
        DataPicker = driver.window_handles[1]
        driver.switch_to.window(DataPicker)
        time.sleep(2)
        if Req == 'GTD':
            driver.find_element_by_xpath(r'//*[contains(@value, "|1|")]').click()
            driver.find_element_by_id('OK').click()        
        
        elif Req == 'GTM':
            driver.find_element_by_xpath(r'//*[contains(@value, "|2|")]').click()
            driver.find_element_by_id('OK').click()
        elif Req == 'NA':
            driver.find_element_by_xpath(r'//*[contains(@value, "||")]').click()
            driver.find_element_by_id('OK').click()
        
        time.sleep(2)
        driver.switch_to.window(MainWindow)
    else:
        print("Unable to select role")

#*End******Adding Role (GTD/GTM) ************************* 

    '''
    time.sleep(1)
    driver.find_element_by_xpath(r'//*[contains(@title, "'+Res+'")]').click()

    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3)
    actions.send_keys(Keys.ENTER)
    time.sleep(2)
    actions.send_keys(SDate)
    time.sleep(2)
    actions.send_keys(Keys.TAB)
    time.sleep(1)
    actions.perform()

    time.sleep(1)
    driver.find_element_by_xpath(r'//*[contains(@title, "'+Res+'")]').click()
    time.sleep(1)

    EndDate = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="taskreserve-0-grid-widget__grid-0"]/div[4]/div[3]/div/div[2]/div[7]/div')))
    EndDate.click()
    actions = ''
    actions = ActionChains(driver)
    time.sleep(1)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(EDate)
    time.sleep(1)
    actions.perform()


    Utilization = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@id="taskreserve-0-grid-widget__grid-0"]/div[4]/div[3]/div/div[2]/div[10]/div')))
    Utilization.click()
    actions = ''
    actions = ActionChains(driver)
    time.sleep(1)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(str(UT))
    time.sleep(1)
    actions.perform()




def mainFasterr(WP):

    workbook = xlrd.open_workbook(r'C:\Users\sahusub\Desktop\TestData.xlsx')
    sheet = workbook.sheet_by_name("Data1")
    rowcount = sheet.nrows
    colcount = sheet.ncols
    SD1 = ED1 = UT1 = SD2 = ED2 = UT2 = SD3 = ED3 = UT3 = SD4 = ED4 = UT4 = SD5 = ED5 = UT5 = SD6 = ED6 = UT6 = ''
    global row1
    row1 = []
    global row2
    row2 = []
    global row3
    row3 = []
    global row4
    row4 = []
    global row5
    row5 = []
    global row6
    row6 = []
    for r in range(rowcount):
        for c in range(colcount):
            if sheet.cell_value(r, c) == WP:

                Res1 = sheet.cell_value(r, c+1)
                if Res1 != '':
                    SD1 = sheet.cell_value(r, c+2)
                    SD1 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD1, workbook.datemode))
                    SD1 = SD1.strftime('%d/%m/%y')
                    ED1 = sheet.cell_value(r, c+3)
                    ED1 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED1, workbook.datemode))
                    ED1 = ED1.strftime('%d/%m/%y')
                    UT1 = sheet.cell_value(r, c+4)
                    UT1 = float(UT1*100)
                    REQ1 = sheet.cell_value(r, c+5)
                    row1.append(Res1)
                    row1.append(SD1)
                    row1.append(ED1)
                    row1.append(UT1)
                    row1.append(REQ1)

                Res2 = sheet.cell_value(r+1, c+1)
                if Res2 != '':
                    SD2 = sheet.cell_value(r+1, c+2)
                    SD2 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD2, workbook.datemode))
                    SD2 = SD2.strftime('%d/%m/%y')
                    ED2 = sheet.cell_value(r+1, c+3)
                    ED2 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED2, workbook.datemode))
                    ED2 = ED2.strftime('%d/%m/%y')
                    UT2 = sheet.cell_value(r+1, c+4)
                    UT2 = float(UT2*100)
                    REQ2 = sheet.cell_value(r+1, c+5)
                    row2.append(Res2)
                    row2.append(SD2)
                    row2.append(ED2)
                    row2.append(UT2)
                    row2.append(REQ2)

                Res3 = sheet.cell_value(r+2, c+1)
                if Res3 != '':
                    SD3 = sheet.cell_value(r+2, c+2)
                    SD3 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD3, workbook.datemode))
                    SD3 = SD3.strftime('%d/%m/%y')
                    ED3 = sheet.cell_value(r+2, c+3)
                    ED3 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED3, workbook.datemode))
                    ED3 = ED3.strftime('%d/%m/%y')
                    UT3 = sheet.cell_value(r+2, c+4)
                    UT3 = float(UT3*100)
                    REQ3 = sheet.cell_value(r+2, c+5)
                    row3.append(Res3)
                    row3.append(SD3)
                    row3.append(ED3)
                    row3.append(UT3)
                    row3.append(REQ3)

                Res4 = sheet.cell_value(r+3, c+1)
                if Res4 != '':
                    SD4 = sheet.cell_value(r+3, c+2)
                    SD4 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD4, workbook.datemode))
                    SD4 = SD4.strftime('%d/%m/%y')
                    ED4 = sheet.cell_value(r+3, c+3)
                    ED4 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED4, workbook.datemode))
                    ED4 = ED4.strftime('%d/%m/%y')
                    UT4 = sheet.cell_value(r+3, c+4)
                    UT4 = float(UT4*100)
                    REQ4 = sheet.cell_value(r+3, c+5)
                    row4.append(Res4)
                    row4.append(SD4)
                    row4.append(ED4)
                    row4.append(UT4)
                    row4.append(REQ4)

                Res5 = sheet.cell_value(r+4, c+1)
                if Res5 != '':
                    SD5 = sheet.cell_value(r+4, c+2)
                    SD5 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD5, workbook.datemode))
                    SD5 = SD5.strftime('%d/%m/%y')
                    ED5 = sheet.cell_value(r+4, c+3)
                    ED5 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED5, workbook.datemode))
                    ED5 = ED5.strftime('%d/%m/%y')
                    UT5 = sheet.cell_value(r+4, c+4)
                    UT5 = float(UT5*100)
                    REQ5 = sheet.cell_value(r+4, c+5)
                    row5.append(Res5)
                    row5.append(SD5)
                    row5.append(ED5)
                    row5.append(UT5)
                    row5.append(REQ5)

                Res6 = sheet.cell_value(r+5, c+1)
                if Res6 != '':
                    SD6 = sheet.cell_value(r+5, c+2)
                    SD6 = datetime.datetime(
                        *xlrd.xldate_as_tuple(SD6, workbook.datemode))
                    SD6 = SD6.strftime('%d/%m/%y')
                    ED6 = sheet.cell_value(r+5, c+3)
                    ED6 = datetime.datetime(
                        *xlrd.xldate_as_tuple(ED6, workbook.datemode))
                    ED6 = ED6.strftime('%d/%m/%y')
                    UT6 = sheet.cell_value(r+5, c+4)
                    UT6 = float(UT6*100)
                    REQ6 = sheet.cell_value(r+5, c+5)
                    row6.append(Res6)
                    row6.append(SD6)
                    row6.append(ED6)
                    row6.append(UT6)
                    row6.append(REQ6)

    openWP(WP)
    if len(row1) != 0:
        addResource(row1[0])
        if len(row2) != 0:
            addMultResource(row2[0])
            if len(row3) != 0:
                addMultResource(row3[0])
                if len(row4) != 0:
                    addMultResource(row4[0])
                    if len(row5) != 0:
                        addMultResource(row5[0])
                        if len(row6) != 0:
                            addMultResource(row6[0])

    driver.switch_to_default_content()
    OKButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, 'OK')))
    OKButton.click()

    MainWindow = driver.window_handles[0]
    driver.switch_to_window(MainWindow)

    addUtilization(Res1, SD1, ED1, UT1, REQ1)
    if Res2 != '':
        addUtilization(Res2, SD2, ED2, UT2, REQ2)
        if Res3 != '':
            addUtilization(Res3, SD3, ED3, UT3, REQ3)
            if Res4 != '':
                addUtilization(Res4, SD4, ED4, UT4, REQ4)
                if Res5 != '':
                    addUtilization(Res5, SD5, ED5, UT5, REQ5)
                    if Res6 != '':
                        addUtilization(Res6, SD6, ED6, UT6, REQ6)

    DownButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, r'//*[@class="dock-bottom-icon"]')))
    DownButton.click()
    print('WP Finished', WP)


def runScript():

    workbook = xlrd.open_workbook(r'C:\Users\sahusub\Desktop\TestData.xlsx')
    sheet = workbook.sheet_by_name("Data")
    rowcount = sheet.nrows
    colcount = sheet.ncols
    WP_Code = []
    for curr_row in range(1, rowcount, 1):
        for curr_col in range(0, 1, 1):
            data = str(sheet.cell_value(curr_row, curr_col))
            WP_Code.append(data)
        # print(WP_Code)
        print(WP_Code[-1])
        mainFasterr(WP_Code[-1])
        time.sleep(2)



loginForDEVQA()
runScript()

