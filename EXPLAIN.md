## Initial thoughts

I was curious to see what I was working with and honestly wasn't expecting aws access keys to be in the prompt. The most important thing to me at that point was looking to see what kind of data the bucket had in store for me.

## Looking at the files

I wasn't expecting the data to be in a json format. So the first thing I did was work out of a notebook to convert it into a pandas dataframe. This helped me get a clearer picture of what exactly I was looking at. This also helped me organize my thoughts on how I wanted to approach this. The movie details file however was a different story. This was nowhere close to clean; by that I mean the values were in a lot of different formats. There were word and numeric value, different currencies, and just a lot of "noise" in general.

## Approach

I went for the simple approach where I just grabbed whatever I need and cut everything else. I had to add different catches to address all the problematic cases. I first add a condition where there needs to be a budget value for the film. My first concern was converting all the currencies into USD. I converted the values based on the exchange rate of when I received the prompt (6/19/21). Then I wanted to check which ones did not have the '$' symbol as the first character since some values were "US$X,XXX,XXX". I worked on just completely removing everything but the number itself. For the word values; I converted them to a numeric format. Throughout all my catches; if a range was given, it would selected the high value.
