# Analysis and metric generation of climbing logs

## Context
You are logging your indoor climbing sessions for further analysis.  These logs only contain high-level information on which routes you climbed during the session, their order and the ascent type.  Ideally, these logs should be sufficient to generate meaningful performance metrics or actionable insights.

## Example of the data
The logs are currently containing the following information:

Date | Climbing gym | # in session | Route ID | Difficulty lvl | Send type | Style | Route info | # Blocks | # Falls | # Sends | Notes
---- | ------------ | ------------ | -------- | -------------- | --------- | ----- | ---------- | -------- | ------- | ------- | -----
14/11/2022 | XX | 1 | 1234 | 5.11d | Redpoint | Lead | roof | 0 | 0 | 1 | Hard crux
14/11/2022 | XX | 2 | 1235 | 5.10d | Onsight  | Toprope | arrete | 0 | 0 | 1 | 
15/11/2022 | YY | 1 | 2345 | 6a | Redpoint | Toprope | | 0 | 0 | 3

In addition, the high-level attributes of climbing sessions are also logged.  An example of these are:

Date | Climbing gym | Warm-up | Stretching | Exercises at end | Start time | End time | Notes
---- | ------------ | ------- | ---------- | ---------------- | ---------- | -------- | -----
14/11/2022 | XX | No | Yes | No | 14:00 | 17:00
15/11/2022 | YY | Yes | No | No | 10:00 | 12:00

Additional information on the height of the climbing walls, average angle of a given wall, ... should perhaps also be compiled.

## Metrics to compute
While the main focus of the logged climbs is to compute climbing performance, the dataset can also serve as the source for other / additional metrics.  Moreover, a breakdown between toprope and lead ascents could be warranted for additional information.

### Performance
There seems to be no concensus on which metrics are most indicative of climbing performance.  At least not directly from the climbing ascents themselves...  - Google searches, a.k.a. research, will regularly be conducted to corroborate this. -  Still, the maximum onsight level seems to be a good proxy to the actual "climbing level" of someone.  Yet, there are also inherent problems with this.

First, new routes are set with a fixes schedule at climbing gyms.  Hence, there might not be any routes available to onsight at a given moment in the climbing gym.  As such, a sufficiently large time interval needs to be considered to determine the number of / maximum level of onsight ascents. Secondly, it might not be possible to "properly" onsight some routes as you might see someone climbing the route / getting stuck on a crux.  For simplicity, "flash" ascents are considered onsights ascents in this dataset.

Websites like [8a.nu](https://8a.nu) also provide route / grade pyramids.  Such pyramids are a visually representation of all ascents with respect to their ascent type and difficulty level.  As such, they could be good for dashboarding / visualizations of the climbing performance.

![Professional climber Adam Ondra's grade pyramid](https://d3byf4kaqtov0k.cloudfront.net/news/636551553626856862_Namnl%C3%B6s.jpg)

_Figure: Professional climber Adam Ondra's grade pyramid_

### Intensity
Similarly to performance, there is no dedicated metric that summarizes the climbing intensity correctly.  At first glance, the climbing intensity depends on the following variables:

- number of climbing sessions per date range
- number of ascents per climbing session
- characteristics of each ascent, such as grade and incline

In addition, some secondary variables also contribute to the intensity:

- rest time between climbing sessions
- rest time between routes (not logged!)
- overal physique that day (tiredness, stress, ...)

All the dependencies (and those missed) on the climbing intensity are currently ignored.  As a first analysis / effort, the following metrics are selected.  These are computed per date range (for example per week or per month) and per climbing session (except number of climbing sessions):

- number of climbing sessions
- number of unique ascents (which ignores resistance / endurance training routes)
- number of ascents (accounts for resistance / endurance training routes)
- grade pyramid, which summarizes the minimum, average, median, and maximum grade per date range
- number of falls / blocks

### Warm-up sequence
TBD

- Can you determine an ideal / bad warm-up sequence?
- Can you warm up too much?

### Climbing style
TBD

- Do you have a preferred style of climbing by climbing more of these?  Is it an observation bias due to the gym?
- Do you perform better on certain climbing styles?  Assuming there is no observation / selection bias by the climber.

### Resistance / Endurance
TBD

- How do you account for resistance / endurance ascents, where a single route is repeated several times without (or minimal) resting?

### Dedicated sessions
TBD

- Can you determine a session type from the logs?

## Sources
- [8a.nu: Article on the wide route pyramid of professional climber Adam Ondra](https://www.8a.nu/news/wide-pyramid-long-time-success-lifestyle)
- [Power Company: Non-ascent climbing metrics for climbers](https://www.powercompanyclimbing.com/blog/metrics-for-climbers)
- [Power Company: Non-ascent climbing metrics for climbers and how to improve](https://www.powercompanyclimbing.com/blog/climb-harder-data)
- [Finger strength analysis tool](https://strengthclimbing.com/finger-strength-analyzer/)
- [Conversion between the different climbing grades](http://www.alpinist.com/p/online/grades)