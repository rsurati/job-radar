from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
#chrome_options.add_argument("--start-maximized")  # Run headless Chrome, without opening a window

# Specify the path to chromedriver if it's not in your PATH
path1 = "C:\\Program Files\\Google\\Chrome\\chromedriver_win32\\chromedriver.exe"
service = Service(path1)

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

