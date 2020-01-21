from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import collections

class InstaBot:
    
    def __init__(self, username, password):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        #add chrome webdriver file path
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get("https://www.instagram.com/")
        sleep(2)

        #log in
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[2]/p/a")\
            .click()
        sleep(2)
        #username
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")\
            .send_keys(username)
        #password
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")\
            .send_keys(password)
        #submit
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]")\
            .click()
        sleep(4)
        #scroll
        self.driver.execute_script("scroll(0, -250);")
        #click profile
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]")\
            .click()
        sleep(2)

    def get_like_stats(self):
        prevLikes = self._get_prev_likes()
        #get new post likes
        newPic = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]')
        newPicLikes = self._get_pic_likes(newPic)
        print("Collected likes for most recent post\n")
        #get frequency of likes
        freq = collections.Counter(prevLikes)
        #print list that normally likes
        print("Frequent but missing:\n")
        for key, value in freq.items():
            if value >=4 and key not in newPicLikes:
                print(key)
        #print list that does not normally like
        print("\nInfrequent but present:\n")
        for key, value in freq.items():
            if value <=1 and key in newPicLikes:
                print(key)

    def _get_prev_likes(self):
        #get likes for 5 previous posts
        pic5 = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/div[3]')
        likes5 = self._get_pic_likes(pic5)
        print("Collected likes for 1/5 last posts")
        pic4 = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/div[2]')
        likes4 = self._get_pic_likes(pic4)
        print("Collected likes for 2/5 last posts")
        pic3 = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/div[1]')
        likes3 = self._get_pic_likes(pic3)
        print("Collected likes for 3/5 last posts")
        pic2 = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[3]')
        likes2 = self._get_pic_likes(pic2)
        print("Collected likes for 4/5 last posts")
        pic1 = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[2]')
        likes1 = self._get_pic_likes(pic1)
        print("Collected likes for 5/5 last posts")
        #extend lists
        likes5.extend(likes4)
        likes5.extend(likes3)
        likes5.extend(likes2)
        likes5.extend(likes1)
        return likes5

    def _get_pic_likes(self, pic):
        self.driver.execute_script('arguments[0].scrollIntoView()', pic)
        #click pic
        pic.click()
        sleep(1)
        #click likes
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button")\
            .click()
        sleep(1)
        #collect names
        names = self._get_names()
        #Back to photos
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/button")\
            .click()
        self.driver.find_element_by_xpath("/html/body/div[4]/button[1]")\
            .click()
        return names
        

    def _get_names(self):
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")
        users = []
        last_ht, ht = 0, 1
        while last_ht != ht:
            buffer = scroll_box.find_elements_by_tag_name('a')
            try:
                names = [name.text for name in buffer if name.text != '']
            except:
                continue
            last_ht = ht
            sleep(1)
            #scroll to bottom of box and return height
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
            for i in names:
                if i not in users:
                    users.append(i)
        return users
        
bot = InstaBot('username', 'password')
bot.get_like_stats()

