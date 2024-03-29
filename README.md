# [mo2.info](https://app.mo2.info)
Many of the systems in [Mortal Online 2](https://www.mortalonline2.com/)
are undocumented, leaving players to experiment and discover on their own.
The goal of this project is to facilitate data-driven 
analysis of the game, producing online calculators that update their 
predictions automatically as new data comes in.

## Overview
Let's begin with an example: Given the in-game tooltip stats for a bow, 
how much damage will that bow do per shot on average to an unarmored 
target dummy? 

Many players know that the `Range` stat is a key indicator of the relative
damage of different bows, but don't know exactly how much damage a given bow
can do in *absolute* terms. If we assume that damage is a linear function of
range (provided that the player has maxed out all the relevant archery stats),
it should be simple to build a bow damage calculator using plain old
OLS regression. 

So, bow damage estimation is the first system that's been modeled in this 
project. The [`BowDamageTrial`](mo2info/main/models.py) data model represents
one trial of a simple experiment: record the key tooltip stats, shoot a few
arrows into a target dummy, and note the damage. The web app provides a 
form to contribute data.

In order to turn that raw data into a predictive model, a 
[`BowDamagePredictor`](mo2info/main/models.py) can define a regression `formula`
like `mean_damage ~ range` (i.e., mean damage is a function of range). 

The predictor instances can also define a `queryset_filter` to limit the input data
used for fitting the predictive model. For instance, the range-to-damage function
when using longbow arrows is different than when using broadhead arrows, so we have 
two different `BowDamagePredictor` instances: one for longbows (which use longbow arrows),
and another for short and asymmetric bows (which use broadhead arrows).

Once these predictors are defined and fit to the empirical data, they can be used
to calculate bow damage from range.

The predictive model is fit using the `statsmodels.formula` API for OLS regression
and cached to minimize repeated calculations. Whenever a new `BowDamageTrial` is 
recorded, the cache is busted and the model will be recalculated the next time it's 
used.

## Project Status and Roadmap
This is currently **the very first proof-of-concept version** of this app. There is 
a lot that still needs to be done:
- [X] **Initial backend**: Able to collect data about a game subsystem and turn
it into a predictive model that is continuously updated as new data comes in.
- [ ] **Initial frontend**: Replace the old-school vanilla Django template system 
with a user-friendly frontend React client. Convert the backend to a 
Django Rest Framework project providing a JSON API.
- [ ] **Continuous deployment**: GitHub Actions are already used to run PR tests, 
but need additional configuration to actually deploy to AWS (currently must be
deployed via command line by the project owner). There is also currently no
mechanism to deploy static files, which will be required for the frontend.
- [ ] **Improved development environment**: You can clone this repo and simply
`cd dev && docker-compose up` to bring up a Docker dev environment, but it 
currently takes some hand-holding to get your local DB into shape, create migrations,
etc. It could also be re-worked to cache dependencies to a `.venv` volume to make
builds much faster.
- [ ] **Broaden scope**: Bow damage calculation is just one of many subsystems in
the game that could be modeled. Design more experiments and increase the number
of calculators available. (This will probably be the bulk of work on this project
in the long run.)
- [ ] **Expand model types**: OLS regression will answer a lot of questions, but more
sophisticated predictive models might be needed for some systems.
- [ ] **Dynamic model selection**: Rather than hard-coding which predictive model
to use for a certain system, dynamically select the best among competing
models.

## How to Build a New Calculator
1. Define a data model to collect experimental trials, similar to 
[`BowDamageTrial`](mo2info/main/models.py).
2. Create a subclass of `CachedPredictor` that can model the data you collected (e.g., 
a new subclass of [`CachedOLSPredictor`](mo2info/main/models.py)).
3. Define [`View`s](mo2info/main/views.py) to collect data and produce a prediction.
