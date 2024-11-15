# -*- coding: utf-8 -*-
"""Spark_Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15CFidR9lg8Pn-9hllt77Vu3o_xkQR0QG

# **Welcome to the Notebook**

### Let's mount the google drive
"""
!pip install google
from google.colab import drive
drive.mount('/content/drive')

"""# Task 1 :
Installing pyspark module
"""

!pip install pyspark

"""Importing the modules"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import count, desc , col, max,struct
import matplotlib.pyplot as plts

"""creating spark session"""

spark=SparkSession.builder.appName('spark_app').getOrCreate()

"""# Task 2 :
importing the *Listenings.csv* file:
"""

listening_csv_path='/content/drive/MyDrive/dataset/listenings.csv'
listening_df=spark.read.format('csv').option('inferSchema',True).option('header',True).load(listening_csv_path)

"""let's check the data:"""

listening_df.show()

"""let's delete useless columns:"""

listening_df=listening_df.drop('date')

"""drop the null rows:"""

listening_df=listening_df.na.drop()

"""let's check the dataset again:"""

listening_df.show()

"""let's see the schema:"""

listening_df.printSchema()

"""let's see the shape of our dataframe:"""

shape=(listening_df.count(),len(listening_df.columns))
print(shape)

"""# Task 3:

**Query #0:**
select two columns: track and artist
"""

q0=listening_df.select('artist','track')
q0.show()

"""**Query #1**:

Let's find all of the records of those users who have listened to ***Rihanna***
"""

q1=listening_df.select('*').filter(listening_df.artist=='Rihanna')
q1.show()

"""**Query #2:**

Let's find top 10 users who are fan of ***Rihanna***
"""

q2=listening_df.select('user_id').filter(listening_df.artist=='Rihanna').groupby('user_id').agg(count('user_id').alias('count')).orderBy(desc('count')).limit(10
                                                                                                                                                              )
q2.show()

"""**Query #3:**

find top 10 famous tracks
"""

q3=listening_df.select('artist','track').groupby('artist','track').agg(count('*').alias('count')).orderBy(desc('count')).limit(10)
q3.show()

"""**Query #4:**

find top 10 famous tracks of ***Rihanna***
"""

q4=listening_df.select('track','artist').filter(listening_df.artist=='Rihanna').groupby('track','artist').agg(count('*').alias('count')).orderBy(desc('count'))
q4.select('track','count').limit(10).show()

"""**Query #5:**

find top 10 famous albums
"""

q5=listening_df.select('artist','album').groupby('album').agg(count('*').alias('count')).orderBy(desc('count')).limit(10)
q5.show()

"""# Task 4 :
importing the ***genre.csv*** file:
"""

genre_csv_path='/content/drive/MyDrive/dataset/genre.csv'
genre_df=spark.read.format('csv').option('inferSchema',True).option('header',True).load(genre_csv_path)

"""let's check the data"""

genre_df.show()

"""Let's inner join these two data frames"""

data=listening_df.join(genre_df,how='inner',on='artist')
data.show()

"""**Query #6**

find top 10 users who are fan of ***pop*** music
"""

data.columns



"""**Query #7**

find top 10 famous genres
"""

q6=data.select('user_id','genre').filter(data.genre=='pop').groupby('user_id').agg(count('*').alias('count')).orderBy(desc('count')).limit(10)
q6.show()

"""# Task 5:
**Query #8**

find out each user favourite genre
"""

q8=data.select('user_id','genre').groupby('user_id','genre').agg(count('*').alias('count')).orderBy('user_id')
q8.show()

q8_2=q8.groupby('user_id').agg(max(struct(col('count'),col('genre'))).alias('max'))

q8_2=q8_2.select('user_id',col('max.genre'))
q8_2.show()



"""**Query #9**

find out how many pop,rock,metal and hip hop singers we have

and then visulize it using bar chart
"""

q9=data.select('user_id','genre').filter((col('genre') =='pop')|(col('genre') =='rock')|(col('genre') =='metal') |(col('genre') =='hip hop')).groupby('genre').agg(count('genre').alias('count'))
q9.show()
q9_list=q9.collect()
lables=[row['genre']for row in q9_list]
counts=[row['count']for row in q9_list]

counts=[row['count']for row in q9_list]

"""Now, let's visualize the results using ***matplotlib***"""







"""now lets visualize these two lists using a bar chart"""

plts.bar(lables,counts)