import codecademylib
import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')

print(ad_clicks.head())

#Which ad platform is getting the most views?
max_views = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(max_views)
#Google has the most views at 680.

#Creating new column to check the valid ad clicks according to whether ad_click_timestamp is a null value or not.
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

#Getting percent of people who clicked on ads from each utm_source
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print(clicks_by_source)

#Pivoting the data
clicks_pivot = clicks_by_source.pivot(columns = 'is_click', index = 'utm_source', values = 'user_id').reset_index()
print(clicks_pivot)

clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])
print(clicks_pivot)

##ANALYZING AN A/B TEST
ad_group = ad_clicks.groupby('experimental_group').user_id.count().reset_index()
print(ad_group)
#The same number of people was shown both ads(827)

#Checking to see if a greater percentage of users clicked on ad A or ad B
ad_click_count = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
#Pivoting
ad_click_count_pivot = ad_click_count.pivot(columns = 'is_click', index = 'experimental_group', values = 'user_id').reset_index()
print(ad_click_count_pivot)
#More users clicked ad A than ad B

#Did the clicks change by day of week?
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']
a_clicks_count = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
a_clicks_pivot = a_clicks_count.pivot(columns = 'is_click', index = 'day', values = 'user_id').reset_index()
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])
print(a_clicks_pivot)

b_clicks_count = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index()
b_clicks_pivot = b_clicks_count.pivot(columns = 'is_click', index = 'day', values = 'user_id').reset_index()
b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])
print(b_clicks_pivot)

#Comparing results
#Percent of users who clicked on the ad by day is greater in group A than B.
#Recommendation
#The company should use ad A.

