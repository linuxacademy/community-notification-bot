from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import chromedriver_binary  # Adds chromedriver binary to path.
import time
import random
import pw
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


USERNAME = pw.USERNAME
PASSWORD = pw.PASSWORD
email = USERNAME
password = PASSWORD
send_to_email = USERNAME
subject = 'New Post Needs Congratulating'

START_URL = 'https://linuxacademy.com/cp/socialize'
   
# Initialize Chrome WebDriver options.
driver_options = webdriver.ChromeOptions()
#driver_options.add_argument('--headless')
driver_options.add_argument('--lang=en')
driver_options.add_argument("--no-sandbox")
#driver_options.add_argument(user_agent)
# Initialize Chrome WebDriver.
driver = webdriver.Chrome(options=driver_options)
# Entire DOM loading timeout.
driver.set_page_load_timeout(60)
# Page element loading timeout.
driver.implicitly_wait(30)
print("Chrome WebDriver Initialized.")

driver.get(START_URL)
print("Loaded page: {}".format(driver.current_url))

# LOG IN WITH GOOGLE.
print("Logging in with Google.")
driver.find_element_by_xpath('//*[@data-provider="google-oauth2"]').click()
# find email text box.
email_path_ele = driver.find_element_by_xpath('//input[@type="email"]')
# enter email text.
email_path_ele.send_keys(USERNAME)
# click next button.
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
# find password text box.
time.sleep(4)
email_path_ele = driver.find_element_by_xpath('//input[@type="password"]')
# enter password text.
email_path_ele.send_keys(PASSWORD)
# click next button.
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()

# return True if it finds posts to reply to, False if they are all replied to.
def reply_to_unreplied():
    # Find list of achievement posts. Slowly scroll down the page so all posts load.
    print("Searching for achievement posts.")
    all_achievement_posts = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        achievement_posts_ids = [ele.get_attribute('id') for ele in driver.find_elements_by_xpath('//*[@class="achievement-callout"]/parent::*[@class="achievement-post-template card"]')]
        for post_id in achievement_posts_ids:
            if post_id not in all_achievement_posts:
                print(f"Found new post id: {post_id}")
                all_achievement_posts.append(post_id)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height: break
        last_height = new_height
    print("Found {} total achievement posts.".format(len(all_achievement_posts)))
    print("Checking for posts not replied to.")
    num_replies = 0
    for post_id in reversed(all_achievement_posts):
        post_ele = driver.find_element_by_id(post_id)
        driver.execute_script("arguments[0].scrollIntoView();", post_ele)
        if len(post_ele.find_elements_by_xpath('.//*[@class="personally_replied_flag"]')) == 0:
            print(f"Found unreplied to post: {post_id}")
            print("Seaching for person name.")
            person_name = post_ele.find_element_by_xpath('.//*[@class="post-author-profile-link"]/span').text.strip()
            print("Found name: {}".format(person_name))
            url = "https://linuxacademy.com/cp/socialize/index/type/community_post/id/" + post_id
            messageHTML = person_name + ' has a post that you have not yet congratulated at ' + url
            msg = MIMEMultipart('alternative')
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(messageHTML, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()            

            num_replies += 1
        else:
            print(f"Found already replied to post: {post_id}. Skipping.")

    if num_replies > 0:
        print("Replied to {} posts.".format(num_replies))
        # refresh page and check again.
        print("Refreshing page.")
        driver.refresh()
        # call again to make sure everything is replied to.
        reply_to_unreplied()
    else:
        print("No new posts to reply to. Exiting.")

reply_to_unreplied()