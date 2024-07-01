#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import string
from datetime import datetime, timedelta


# In[2]:


from faker import Faker

fake = Faker("ru_RU")


# In[3]:


class RawData:
    def __init__(self, raw_data_id, data_source, data_content, collection_date):
        self.raw_data_id = raw_data_id
        self.data_source = data_source
        self.data_content = data_content
        self.collection_date = collection_date

class CleanedData:
    def __init__(self, cleaned_data_id, raw_data_id, created_by, cleaned_content, cleaning_date):
        self.cleaned_data_id = cleaned_data_id
        self.raw_data_id = raw_data_id
        self.created_by = created_by
        self.cleaned_content = cleaned_content
        self.cleaning_date = cleaning_date
        
class Task:
    def __init__(self, task_id, assigned_to, task_description, status, due_date, completion_time, reworks):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.task_description = task_description
        self.status = status
        self.due_date = due_date
        self.completion_time = completion_time
        self.reworks = reworks
        
class Report:
    def __init__(self, report_id, cleaned_data_id, user_id, task_id, approved_by, content, creation_date):
        self.report_id = report_id
        self.cleaned_data_id = cleaned_data_id
        self.user_id = user_id
        self.task_id = task_id
        self.approved_by = approved_by
        self.content = content
        self.creation_date = creation_date


class Recommendation:
    def __init__(self, recommendation_id, user_id, approved_by, report_id, task_id, content, creation_date):
        self.recommendation_id = recommendation_id
        self.user_id = user_id
        self.approved_by = approved_by
        self.report_id = report_id
        self.task_id = task_id
        self.content = content
        self.creation_date = creation_date

class Strategy:
    def __init__(self, strategy_id, report_id, recommendation_id, task_id, user_id, content, creation_date):
        self.strategy_id = strategy_id
        self.report_id = report_id
        self.recommendation_id = recommendation_id
        self.task_id = task_id
        self.user_id = user_id
        self.content = content
        self.creation_date = creation_date

class User:
    def __init__(self, user_id, name, role, email):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email


# In[4]:


def generate_random_data(num_entries):
    raw_data_list = []
    cleaned_data_list = []
    task_list = []
    report_list = []
    recommendation_list = []
    strategy_list = []
    user_list = []


    
    for i in range(num_entries):
        user = User(
            user_id=i,
            name=fake.name(),
            role=random.choice(['Руководитель', 'Стратег', 'Аналитик данных', 'Маркетинговый аналитик', 'Помощник', 'SMM-спец', 'SEO-спец']),
            email=fake.email()
        )
        user_list.append(user)

    
    for i in range(num_entries):
        raw_data = RawData(
            raw_data_id=i,
            data_source=fake.company(),
            data_content=fake.text(),
            collection_date=fake.date()
        )
        raw_data_list.append(raw_data)

    
    for i in range(num_entries):
        cleaned_data = CleanedData(
            cleaned_data_id=i,
            raw_data_id=random.choice(raw_data_list).raw_data_id,
            created_by=random.choice(user_list).user_id,
            cleaned_content=fake.text(),
            cleaning_date=fake.date()
        )
        cleaned_data_list.append(cleaned_data)

    for i in range(num_entries):
        task = Task(
            task_id=i,
            assigned_to=random.choice(user_list).user_id,
            task_description=fake.text(),
            status=random.choice(['Pending', 'In Progress', 'Completed']),
            due_date=fake.date(),
            completion_time=random.randint(1, 30),
            reworks=random.randint(0, 5)
        )
        task_list.append(task)
        
    
    for i in range(num_entries):
        report = Report(
            report_id=i,
            cleaned_data_id=random.choice(cleaned_data_list).cleaned_data_id,
            user_id=random.choice(user_list).user_id,
            task_id=random.choice(task_list).task_id,
            approved_by=random.choice(user_list).name,
            content=fake.text(),
            creation_date=fake.date()
        )
        report_list.append(report)

    
    for i in range(num_entries):
        recommendation = Recommendation(
            recommendation_id=i,
            user_id=random.choice(user_list).user_id,
            approved_by=random.choice(user_list).name,
            report_id=random.choice(report_list).report_id,
            task_id=random.choice(task_list).task_id,
            content=fake.text(),
            creation_date=fake.date()
        )
        recommendation_list.append(recommendation)

    
    for i in range(num_entries):
        strategy = Strategy(
            strategy_id=i,
            report_id=random.choice(report_list).report_id,
            recommendation_id=random.choice(recommendation_list).recommendation_id,
            user_id=random.choice(user_list).user_id,
            task_id=random.choice(task_list).task_id,
            content=fake.text(),
            creation_date=fake.date()
        )
        strategy_list.append(strategy)



    return raw_data_list, cleaned_data_list, report_list, recommendation_list, strategy_list, user_list, task_list


# In[5]:


raw_data, cleaned_data, report, recommendation, strategy, user, task = generate_random_data(10)


# In[6]:


print(raw_data[0].__dict__)
print(cleaned_data[0].__dict__)
print(report[0].__dict__)
print(recommendation[0].__dict__)
print(strategy[0].__dict__)
print(user[0].__dict__)
print(task[0].__dict__)


# **Что будем использовать для интегральной метрики:**
# 
# 1. Время на задачу (отдельно для каждого сотрудника).
# 2. Количество возвратов на доработку.
# 3. Общее время выполнения всех задач.
# 4. Количество задач, выполненных без возвратов на доработку

# In[7]:


def integral_metric(tasks, max_allowed_time):
    alpha = 0.5
    beta = 0.5
    
    total_tasks = len(tasks)
    total_time = sum(task.completion_time for task in tasks)
    tasks_without_rework = sum(1 for task in tasks if task.reworks == 0)
    
    average_time = total_time / total_tasks
    time_coefficient = 1 - (average_time / max_allowed_time)
    
    rework_coefficient = tasks_without_rework / total_tasks
    
    integral_metric = (alpha * time_coefficient + beta * rework_coefficient) / (alpha + beta)
    
    return integral_metric


# In[8]:


max_allowed_time = 15


# In[9]:


integral_metric_n = integral_metric(task, max_allowed_time)
print(f"Интегральная метрика: {integral_metric_n:.2f}")


# In[ ]:





# In[ ]:





# In[ ]:




