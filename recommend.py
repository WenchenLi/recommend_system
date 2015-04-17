import graphlab
import datetime
 
import mongodb
import pprint
import json 



# recommend module attach each function with an example after#




def load_data_csv(csv):    
    """input:
    csf file, type str "rating.csv"
    output data for input in build model
    """
    data = graphlab.SFrame.read_csv(csv, column_type_hints={"Rating":int})
    return data
#data = load_data_csv("rating.csv")

def model_create(data):
    """input:
    data from loading_csv
    output:
    constructed model for the rating table including the collaborative filtering matrix
    saved model based on the timestamp
    """
    model = graphlab.recommender.create(data, user_id="UID", item_id="ItemID", target="Rating")
    model.save("my_model"+str(datetime.datetime.utcnow()))
    return model
#model = model_create(data)

def recommend(usersl,n):
    """input:
        usersl:list of user e.g [1,2]
        n: number of item to recommend for each user
        output:
        results for recommend
    """
    results = model.recommend(users=usersl , k=n)
    #results.head()
    return results
results = recommend([1,2],10)

def load_model(model):
    """ input:
    model name in str format
    output:
    loaded model
    """
    loaded_model = graphlab.load_model(model)
    return loaded_model


#recommend to the end user the highest five(default) item in rank calculated in collaborative filtering 

def recommend_json(user,n=None):
    """
    input:
    user: list of user(s) to return result. Example: ["john"]
    n:number of result for each user, default 5
    output:
    itemID: this can be used to retrieve info in item db to get avatar and url for this item for recommend in d3
    item prediciton score for this user 
    # now i choose to save json to the root directory
    {
        "UID":[
        {"ItemID":"1","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"21","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"43","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"45","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"59","Thumbnail":"some image url","Url":"item url"}
        ]
        "UID":[
        {"ItemID":"1","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"21","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"43","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"45","Thumbnail":"some image url","Url":"item url"},
        {"ItemID":"59","Thumbnail":"some image url","Url":"item url"}
        ]...
    }
    """
    if n is None:
        n =5
    
    results = model.recommend(users=user, k=n)
    items = results[:]['ItemID']
    
    item_json = {}
    item_json['UID'] = []
    for b in items:
        for a in mongodb.find_item(int(b)):
            item = {"ItemID":a["ItemID"],"Thumbnail":a["Thumbnail"],"Url":a["Url"]}
            item_json['UID'].append(item)   
        json_data = json.dumps(item_json)  
    with open('json_item.json', 'w') as outfile:
        json.dump(json.loads(json_data), outfile)
    #return json_data

#recommend_json([1])

def similarity(data):
    """
    input:
    data from loading_csv
    output:
    a big table find each item with its similar item(s)
    """
    similar = graphlab.recommender.item_similarity_recommender.create(data,user_id="UID", item_id="ItemID", target="Rating")
    similar_table = similar.get_similar_items()
    return similar_table
#similarity(data)