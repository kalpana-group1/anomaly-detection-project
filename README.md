# Anomaly-detection-project
Codeup anomaly-detection-project


By: Brad Gauvin, Glady Barrios, Kevin Smith

# Project Description 

We have put this notebook to answer the following email:

Email to analyst:


#### Hello,


#### I have some questions for you that I need answered before the board meeting Thursday afternoon. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Anything else I should be aware of?


# Project Goal 

Our project goal is to answer at least five of the questions asked in this email before our deadline so that our representive will have this data avalible in a timely manner.

# Executive Summary

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
 - Data Science frequents Fundamentals
  - Full stack - Java Script 1 

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?


3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
For this question we assummed that "active students" means students who are currenly students and not "alumni".
This is an exploration of the students who only access the curriculm less than 10 times 

 - Students who access the curriculum less than 10 times are all from Full Stack - Java Script
 - These are students in cohorts: Voyageurs, Andromeda, Europa, Ganymede, Hyperion, Jupiter, Marco, Neptune and Oberon.
 - These two cohorts with the largest ammount of students that do not visit the curriculum as often are Andromeda and Hyperion 

4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?

`The short answer is yes to both.`

First our breakdown function calculates the percentage of all the endpoints available that each user_id has accessed. The average user accesses 10% of the sites. So, we set the bar for suspiscous activity at double the average; meaning that any user that has accessed more than 20% of the endpoints is flagged as suspiscious.

The second way we define suspiscious activity is if the user is missing a cohort_id. This could be an input error, or it could be something nefarious. Either way, further exploration of these user_ids is warranted.

The final way we define suspiscious activity is the number of different ip addresses that the user is associated with. The average user is associated with 10 different ip addresses. So, for the sake of simplicity we set the bar for suspiscious at double the average, and anyone who has accessed the site from more than 20 ip addresses is flagged as suspiscious for further investigation.


5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?

`In short, yes it is still happening, and yes it happened before.`

A look into user number 11 shows that there is evidence of the user accessing endpoints that belong to a curriculum that this user did not pay for as recently as 2021. The large spikes in activity coupled with the fact that many of the data science endpoints have only been accessed once suggests that there is webscraping going on. however, further data is needed to be certain of the type of activity that is happening. They could have paid for the course, but not been reclassified as a data science student. Without access to payment records, and more time.


6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
- Full Stack Java- spring, javascript-i, html-css, mysql
- Full Stack PHP - Content, javascript-i, html -css, spring
- Data science- classification, fundimentals, sql, python

7. Which lessons are least accessed?

-Overall the least accessed lesson is examples (behind searches and table of contents)

By program the least accessed lessons are:
- Data Science: classification
- Front-End(no longer offered): Classification
- Full stack (Java): Javascript and Classification/Slides
- Full stack (PhP): Fundamentals and SQL

