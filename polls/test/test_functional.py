import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from polls.models import Question,Choice
from django.utils import timezone
from django.contrib.auth.models import User


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (days < 0 for questions published
    in the past, days > 0 for questions published in the future).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question

def create_choice(choice_text, question: Question):
    return Choice.objects.create(choice_text=choice_text,question=question)

class SeleniumTestCase(LiveServerTestCase):
    username = "admin"
    password = "korn30850"


    def setUp(self):
        self.selenium = webdriver.Chrome(executable_path='/Users/sk/Desktop/chromedriver')
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTestCase, self).tearDown()

    def test_poll(self):
        self.selenium.get(self.live_server_url + '/polls/')
        h1 = self.selenium.find_element_by_tag_name('h1')
        self.assertIn('Welcome back,korn',h1.text)         
                
    def test_poll_question(self): 
        question = create_question("First Question", days=-1)
        self.selenium.get(self.live_server_url + '/polls/')
        element = self.selenium.find_element_by_id(f"q{question.id}")  
        self.assertEqual(element.text,'First Question')   

    def test_question_detail(self):
        question = create_question("First Question", days=-1)
        self.selenium.get(self.live_server_url + '/polls/')
        links = self.selenium.find_elements_by_tag_name('a')
        links[1].click()
        self.assertEqual(self.selenium.current_url,self.live_server_url + '/polls/' + f"{question.id}/")

    def test_question_result(self):
        question = create_question("First Question", days=-1)
        choice = create_choice("First Choice", question)  
        User.objects.create_user(self.username, password=self.password)
        self.selenium.get(self.live_server_url + '/accounts/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id("login").click()
        link = self.selenium.find_element_by_tag_name('a')
        link.click()
        choice1 = self.selenium.find_element_by_id(f"choice{choice.id}")
        choice1.click()
        self.selenium.find_element_by_id(f"vote").click()
        self.assertEqual(self.selenium.current_url,self.live_server_url + '/polls/' + f"{question.id}/results/")