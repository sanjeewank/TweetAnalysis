import snscrape.modules.twitter as sntwitter
import pandas as pd

query = '(Qatar OR Ecuador OR Senegal OR Netherlands OR England OR Iran OR USA OR Wales OR Argentina OR Saudi Arabia OR Mexico OR Poland OR France OR Australia OR Denmark OR Tunisia OR Spain OR Costa OR Rica OR Germany OR Japan OR Belgium OR Canada OR Morocco OR Croatia OR Brazil OR Serbia OR Switzerland OR Cameroon OR Portugal OR Ghana OR Uruguay OR South Korea) (#worldcup2022 OR #worldcup OR #fifa OR #football) lang:en until:2022-12-20 since:2022-11-18'
tweets = []
limit = 2000


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweets.date, tweets.username, tweets.content, tweets.likeCount, tweets.retweetCount, tweets.replyCount,tweets.quoteCount])
        
df = pd.DataFrame(tweets, columns=['date', 'user', 'tweets','favorites', 'retweets', 'reply','response'])
print(df)

# to save to csv
df.to_csv('tweets.csv')