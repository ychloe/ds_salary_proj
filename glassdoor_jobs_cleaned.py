import pandas as pd 
data = pd.read_csv ('C:/Users/chloe/Documents/ds_salary_proj/glassdoor_jobs.csv')
df = pd.DataFrame(data, columns = ['Company Name', 'Job Title']) 
duplicate = df[df.duplicated(['Company Name', 'Job Title'])] 
duplicate=duplicate.sort_values(by=['Company Name'])
data=data.drop_duplicates()
data.columns

#remove null column
data['num_comp']=data['Competitors'].apply(lambda x: 1 if x>0 else 0)
data['num_head']=data['Headquarters'].apply(lambda x: 1 if x>0 else 0)
data = data.drop(['num_comp','Competitors','num_head','Headquarters'],axis=1)

#salary parsing
data['hourly']=data['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
data['employer_provided']=data['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0) 
data=data[data['Salary Estimate']!='-1']
salary=data['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd=salary.apply(lambda x:x.replace('K','').replace('$',''))
min_hr=minus_Kd.apply(lambda x:x.lower().replace('per hour','').replace('employer provided salary:',''))
data['min_salary']=min_hr.apply(lambda x: int(x.split('-')[0]))
data['max_salary']=min_hr.apply(lambda x: int(x.split('-')[1]))
data['avg_salary']=(data.min_salary+data.max_salary)/2


#Company name text only
data['company_text']=data.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)


#state field
data['job_state']=data['Location'].apply(lambda x: x.split(',')[1])
data.job_state.value_counts()
data['job_state'] = data['job_state'].replace([' Arapahoe'],' CO')
#data['same_state']=data.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)


#age of company
data['age']=data.Founded.apply(lambda x: x if x<1 else 2020 - x)


#parsing of job description(python, etc.)
#python
data['python_yn']=data['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
#r studio
data['R_yn']=data['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
#spark

data['spark']=data['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
#aws
data['aws']=data['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
data.aws.value_counts()
#excel
data['excel']=data['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
data.aws.value_counts()

print(data.columns)
data.to_csv('glassdoor_jobs_cleaned.csv',index=False)
