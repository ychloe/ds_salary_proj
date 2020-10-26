<<<<<<< HEAD
=======
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:09:19 2020

@author: chloe
"""
>>>>>>> 9354d7c99f94dec23526a7b6901c80e8443bc2e4
import glassdoor_scraper as gs
import pandas as pd

data=gs.get_jobs("data scientist",1000,False,"C:/Users/chloe/Documents/ds_salary_proj/chromedriver.exe" ,15)
<<<<<<< HEAD
data.to_csv('glassdoor_jobs.csv',index=False)
=======
data.to_csv('glassdoor_jobs.csv',index=False)
>>>>>>> 9354d7c99f94dec23526a7b6901c80e8443bc2e4
