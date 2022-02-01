# Project Computational Science
## The effect of vaccination strategies on COVID-19 spread and death toll
## Description
In the last two years, the whole world has had to deal with the spread of the corona virus. To combat this virus and its mutation, but also possible future viruses, it is essential to research the spread of such viruses.

One of the more important ways to combat the spread of viruses is to use vaccines. Vaccines can have several effects: a vaccinated person is less likely to contract the virus, if a vaccinated person contracts the virus anyways, their symptoms will be less severe and lastly, they are also less likely to propagate the virus.

Since it is practically impossible to vaccinate every person on earth at once, it is important to think about a vaccination strategy: who will be prioritized for vaccinations. We will focus on 3 possible vaccination strategies: randomly pick people to vaccinate, pick those who are more vulnerable to the symptoms of the virus, or pick the people who come in to contact with a lot of others.

We will compare these 3 strategies to each-other and also to a situation where no-one is vaccinated and are interested in the spread of the virus (number of people infected) and the death-toll. We expect that the strategy to vaccinate people that come in to contact with a lot of others will be most effective to mitigate the spread of the virus. We also expect that the strategy of vaccinating vulnerable people will result in the lowest death-toll. Lastly we expect the random vaccination strategy to be less effective in both aspects than the other strategies, but more effective than not vaccinating at all.

## Usage
#### Install dependencies:
```
pip3 install -r requirements.txt
```
#### Reproduce figures:
```
python3 main.py
```
This will reproduce the figures used for the poster from pre-generated data. To recreate the data, see "Repoduce data". Additionally, one can use main.py to create other figures and run some verifications (see comments in main.py for more info). (Note that if data is removed from the stats folder, some figures can not be created anymore.)

#### Reproduce data:
Before running anything please remove already existing data from the stats folder. If this is not done, new data will only be added to the already existing data files, instead of recreating them. Once this is done, run:
```
python3 facebook_tests.py
```
Please note that running this takes a large amount of time. After each 10 simulations a new file is created with data. The name of this file contains the values of all the parameters: vaccination_method, infection_rate, incubation_period, infection_time, vaccination_rate, vaccine_spread_effectivenes and vaccine_mortality_effectiveness.

Additionally one could use the single_facebook_test function to recreate a specific data point. For example, to recreate data of simulation 3 of fb_age_0.1_5_10_25_0.05_0.05.txt, run single_facebook_test("age", 0.1, 5, 10, 25, 0.05, 0.05, 3) in facebook_tests.py.

## Authors and acknowledgment
- Jaron Has
- Koen Hoeberechts
- Sjoerd Dronkers
