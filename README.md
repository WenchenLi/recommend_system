# recommend_system
dependencies:
pymongo
graphlab
flask
d3.js


This is the repo for recording the process of building the complete 
recommendation system from the backend based on mongodb using 
graphlab and pymongo.

recommend.py is the recommendation system I implemented based on graphlab, it is 
mongodb.py is the python script I used to setup the mongodb and specify the schema of the database,
Those file are well documented with examples. 
recommend.ipynb and recommend.ipynb is ipython notebook file that is easy for me to debug my code in 
the corresponding .py file.

server.py is based on flask that I can used to make function call to my database and recommend.py to fetch 
the recommend results. I'm still working on this part and hopefully I will get this running after a week.

recommend.html is my UI of the recommdation system. Currently everything is static you can run that by first
setup the server on local from command line "python -m SimpleHTTPServer" and it can render the top five 
recommended item for the user. Based on each item if you move your mouse to the item, it can render the 
item based recommendation based on the similarity of item.



