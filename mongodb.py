#DB SETUP

from pymongo import MongoClient
import csv
import pprint
import random

## generate musicfan db

client = MongoClient('mongodb://localhost:27017')
db = client.musicfan 

#---------------------------------------------------------------------------------------
#CRUD functionality for recommendation system

def user_create(uid,name,email,pw):
    #schema for user instance
    #UID name email pw 
    #email should be unique
    '''
    input:
    uid = 0
    name = 'john'
    email = 'john@gmail.com'
    pw = 'john1111'
    '''
    User={
    "UID":uid,
    "Name":name,
    "Email":email,
    "PW":pw
    }
    db.user.insert(User)

#db.user.create_index(("Email"),unique=True)


def rating_create(UID,ItemID,time):
    #schema for rating instance
    #UID ItemID rating   (UID and ItemID is primary key)
    # here I set a initial for UID ItemID test time, time can be return from the webpage side
    """
    input:
    UID =  32 
    ItemID =  0
    time = 1600
    """
    
    if time < 5:
        rating = 0
    elif 5<=time and time < 60:
        rating = 1
    elif 60<=time and time < 120:
        rating = 2    
    elif 120<=time and time < 180:
        rating = 3
    elif 180<=time and time  < 240:
        rating = 4
    elif 240<=time :
        rating = 5    
    Rating = {"UID":UID,
              "ItemID":ItemID,
              "Rating":rating}
    db.rating.insert(Rating)

#db.rating.create_index([("UID", pymongo.ASCENDING),("ItemID", pymongo.ASCENDING)],unique=True)

def item_create(itemID,url,avatar):

    #itemID(primary key) url avatar
    """
    input:
    itemID=10
    url ="https://www.udacity.com/course/viewer#!/c-ud032/l-745498943/m-734730655" 
    tn = "http://lh3.ggpht.com/ll9ungBQPIwG1u5WHYyB_q-CO6gAzJC-fT3xotaS5DV3UbNZ7Xdz6b5T3Jpl7aEfmVEY2gjvkkt7KzWVeIo=s0"
    """
    Item = {
    "ItemID":itemID,
    "Url":url,
    "Thumbnail":tn
    }
    db.item.insert(Item)

#db.item.create_index(("ItemID"),unique=True)



#Query in db, notice when we do collaborative filtering, we only need to convert 
#the rating instance from json to csv for graphlab to conduct the computing for the CF matrix. 
#In this context, we only care about query item that we can retrieve to send to recommendation system rendering side.

#query sinlge Item info
def find_item(itemID):
    item =  db.item.find({"ItemID":itemID})
    return item
#find_item(10)

#Update db
def user_update(uid,name=None,email=None,pw=None):
    User = db.user.find_one({"UID":uid})
    if ((name and email and pw )is None):
        raise IOError("Nothing to update.")
    if (name is not None):
        User["Name"] = name
    if (email is not None):
        User["Email"] = email
    if (pw is not None):
        User["PW"]=pw
def item_update(itemID,url=None,avatar=None):
    User = db.item.find_one({"ItemID":itemID})
    if ((url and avartar)is None):
        raise IOError("Nothing to update.")
    if (url is not None):
        User["Url"] = url
    if (avatar is not None):
        User["Avatar"] = avatar
    

def rating_update(uid,itemID,rating):
    User = db.rating.find_one({"UID":uid, "ItemID":itemID})
    User["Rating"]=rating       


#For the remove option, since we value all the info we saved here, this option will be implemented when needed.
#Be careful when remove all, this will cause your entire data lost.
def item_remove_all():
    """
    remove all item in db
    """
    db.item.drop()
def user_remove_all():
    """
    remove all user in db
    """
    db.user.drop() 
def rating_remove_all():
    """
    remove all rating in db
    """
    db.rating.drop()     

#Finish CRUD
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
#Some utils

##the next function need to be implement is the output db.rating to the graphlab in csv format 
def rating_output_csv(db):
    """input:
        db.collection.collection
       output:
        a csv file in the root directory containing UID, ItemID, Rating
    """
    query ={"_id":{"$exists":1}}
    projection ={"_id":0,"UID":1,"ItemID":1,"Rating":1}
    ratings = db.rating.find(query,projection)
    
    with open('rating.csv', 'wb') as csvfile:
        ratingwriter = csv.writer(csvfile)
        ratingwriter.writerow(['UID','ItemID','Rating'])
        for a in ratings:
            ratingwriter.writerow([a["UID"],a["ItemID"],a["Rating"]])
        
def item_output_json(items):
	"""
	input: items, a list of ItemID (['1','2','3','10'])
	output: json for items that contains ItemID, thumbnail and the url 
	"""




# this is used for testing when there is no real data.
def gen_rating(user_numb,item_numb,k):
    """input:
    user_numb: number of user
    item_numb: number of item
    k  is the number of row in the rating collection
    output:
    random table for UID, ItemID, Rating
    rating is within 0-5.
    """
    userids = range(user_numb)
    itemids = range(item_numb)
    rating = range(6)
    for i in range(k):
        uid = random.choice(userids)
        itemid = random.choice(itemids)
        user_rating = random.choice(rating)
        rating_create(uid,itemid,user_rating)   

#Generate a random rating table for test 

def test():
    """
    this is a test for user 2, ingest item data to the db.item
    """
    itemID = 1814
    url ="http://www.amazon.com/1989-Taylor-Swift/dp/B00MRHANNI/ref=pd_sim_m_3?ie=UTF8&refRID=1K8Y170G44FNQP6RA2H5" 
    tn = "http://ecx.images-amazon.com/images/I/41q3uhpDctL._AA160_.jpg"

    item_create(itemID,url,tn)
    ['1814', '6089', '2447', '4005', '4410']

    itemID = 6089
    tn ="http://ecx.images-amazon.com/images/I/61J61fwud1L._AA160_.jpg"
    url="http://www.amazon.com/Cheek-Deluxe-Lady-Gaga/dp/B00MU79IL8/ref=sr_1_1?ie=UTF8&qid=1428964029&sr=8-1&keywords=lady+gaga"
    item_create(itemID,url,tn)

    itemID = 2447
    tn ="http://ecx.images-amazon.com/images/I/616y3gmSmcL._AA160_.jpg"
    url="http://www.amazon.com/The-Lonely-Hour-Deluxe-Edition/dp/B00H3GZMIE/ref=pd_sim_m_2?ie=UTF8&refRID=1G47A5BAXVTPENQKE6AJ"
    item_create(itemID,url,tn)

    itemID = 4005
    tn ="http://ecx.images-amazon.com/images/I/613BBVSBnEL._AA160_.jpg"
    url="http://www.amazon.com/Hybrid-Theory-LINKIN-PARK/dp/B00004Z459/ref=sr_1_1?ie=UTF8&qid=1428964399&sr=8-1&keywords=linkin+park"
    item_create(itemID,url,tn)
    
    itemID = 4410
    tn ="http://ecx.images-amazon.com/images/I/41yfeQmnysL._SX350_PI_PJStripe-Prime-Only-500px,TopLeft,0,0_AA160_.jpg"
    url="http://www.amazon.com/Hunting-Party-Linkin-Park/dp/B00JYKU6BK/ref=sr_1_2?ie=UTF8&qid=1428964432&sr=8-2&keywords=linkin+park"
    item_create(itemID,url,tn)

