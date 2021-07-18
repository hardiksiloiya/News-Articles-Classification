def get_screenshots(webpage):
    '''
    Get the screenshots of the webpage.
    Returns a list of numpy arrays which are the cropped images from the whole screenshot.
    Example:
    images=get_screenshots('www.google.com')
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('load-extension=' + r'1.36.2_0')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    driver=webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.create_options()
    driver.get(webpage)
    driver.execute_script("return window.stop")
    time.sleep(2)
    #add heuristics for popups here
    try:
        driver.find_element_by_xpath('//*[@id="wt-cli-accept-btn"]').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="form_wrap"]/span').click()
    except:
        pass
    try:
        alert=driver.switch_to_alert()
        alert.accept()
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="wt-cli-accept-btn"]').click()
    except:
        pass
    time.sleep(2)
    s = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    height = driver.execute_script("return document.body.scrollHeight")
    required_height=0.70                                     #required_height can be changed to adjust the percentage of the whole page screenshot to be used (1.00 = use whole page)
    driver.set_window_size(1920,required_height*height)                   
   
    time.sleep(2)
    try:
        driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')
    except:
        driver.save_screenshot('web_screenshot.png')


    driver.quit()
    im=cv2.imread("web_screenshot.png")
    i=0
    imlen=int(len(im[:,0,0]))
    im=im[:imlen,:,:]
    images=[]
    while(i<len(im)):
        temp=im[i:i+1500,:,:]
        images.append(temp)
        i=i+1500
    os.remove('web_screenshot.png')
    return images