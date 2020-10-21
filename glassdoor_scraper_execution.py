import glassdoor_scraper as gs
import pandas as pd

data=gs.get_jobs("data scientist",1000,False,"C:/Users/chloe/Documents/ds_salary_proj/chromedriver.exe" ,15)
data.to_csv('glassdoor_jobs.csv',index=False)