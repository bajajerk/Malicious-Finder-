import tweepy
from textblob import TextBlob
import apiai
import json
import requests

# Training done on APIAI  to extract diffferent suspicious keywords in tweets 
APIAI_ACCESS_TOKEN = "65660d7b382b44a997f9d63986395fbb"


ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)


# # Step 1 - Authenticate
# Input your credentials to make it work
consumer_key= ''
consumer_secret= ''
access_token=''
access_token_secret=''
token=''
token_secret=''




auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 3 - Retrieve Tweets

public_tweets = api.search('tarantula',count=100)

# public_tweets = pd.Dataframe(public_tweets)
# count=0

# for tweet in public_tweets:
#     textInside=tweet.text
#     print(tweet.user.screen_name)
#     print ('tweeted');
#     print(textInside);


        


def apiai_response(query, session_id):
    """
    function to fetch api.ai response
    """
    request = ai.text_request()
    request.lang='en'
    request.session_id=session_id
    request.query = query
    response = request.getresponse()
    return json.loads(response.read().decode('utf8'))


def parse_response(response):
    """
    function to parse response and 
    return intent and its parameters
    """
    result = response['result']
    params = result.get('parameters')
    intent = result['metadata'].get('intentName')
    return intent, params

    
def fetch_reply(query, session_id):
    """
    main function to fetch reply for chatbot and 
    return a reply dict with reply 'type' and 'data'
    """
    response = apiai_response(query, session_id)
    intent, params = parse_response(response)
    score =0
    if intent =='spider' or intent =='tarantula':
        if (params['url']):
            score=score+2
        if (params['currency']):
            score=score+2
        if (params['geo-country']):
            score=score+1
        if (params['color']):
            score=score+1
        # if (params['geo-city']):
        #     score=score+2
        if (params['sell']):
            score = score + 2
        if (params['proneCountries']):
            score=score+3
        if (params['connectme']):
            score=score+5
        if (params['sciname']):
            score=score+4
          
    # if(params['geo-country']==''):
    #   print "COUNtry not found"
    # if intent == None:
    #   reply['type'] = 'none'
    #   reply['data'] = "I didn't understand"

   

    return  score


for tweet in public_tweets:
    
    score=fetch_reply(tweet.text,12)
    # # if (params['currency']!=''):
    # #     score=score+2
    # if (params['geo-country']!=''):
    #     score=score+1
    # if (params['color']!=''):
    #     score=score+1
    # if (params['geo-city']!=''):
    #     score=score+2
    # if (params['sell']!=''):
    #     score = score + 2
    # if (params['proneCountries']!=''):
    #     score=score+3
    # if (params['connectme']!=''):
    #     score=score+5
    # if (params['sciname']!=''):
    #     score=score+4
    
    if (score >2):
        print ("Suspicious Tweet   "+tweet.text)
        print('\n')
        print("***************************8")
        # print(tweet.text)
    # print (score)

    # if(score>2):
    #     print("Its suspicious")
    #     print (tweet.text)
    # # print fetched



























# for tweet in public_tweets:
#     print(tweet.text)
#     ans = fetch_reply(tweet.text,12)
#     print(ans)
