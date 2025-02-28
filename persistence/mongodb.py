from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from AtlasClient import AtlasClient

from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DBNAME = os.getenv('MONGODB_DBNAME')
MONGODB_COLLECTIONNAME = os.getenv('MONGODB_COLLECTIONNAME')


def ping_server(mongodb_uri: str, mongodb_dbname: str):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.ping_server
    if res:
        print("Ping success!")
    else:
        print("No ping!")

def insert_many(mongodb_uri: str, mongodb_dbname: str, quiz_items):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.insert(MONGODB_COLLECTIONNAME, "many", quiz_items)
    if res:
        print("Insert succees!")
    else:
        print("No success!")

def insert_one(mongodb_uri: str, mongodb_dbname: str, quiz_item):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.insert(MONGODB_COLLECTIONNAME, "one", quiz_item)
    if res:
        print("Insert one succees!")
    else:
        print("No success!")

def drop_collection(mongodb_uri: str, mongodb_dbname: str, mongodb_collectionname: str):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.drop_collection(mongodb_collectionname)
    if res:
        print("Drop succees!")
    else:
        print("No success!")

def get_quizzes(mongodb_uri: str, mongodb_dbname: str, mongodb_collectionname: str):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.get_quizes(mongodb_collectionname)
    
    if res is not None:
        for r in res:
            print(f"Quiz Name: {r['name']} | Video Id: {r['video_id']} | Quiz Type: {r['type']} | Number of Q: {r['number_questions']}")
            print([x for x in r['questions']])
            print("--")
    else:
        print("No Quizzes have been found")

def get_quiz(mongodb_uri: str, mongodb_dbname: str, mongodb_collectionname: str, criteria: dict):
    ac = AtlasClient(mongodb_uri, mongodb_dbname)
    res = ac.get_quiz(mongodb_collectionname, criteria)

    if res is not None:
        print(f"Quiz Name: {res['name']} | Video Id: {res['video_id']} | Quiz Type: {res['type']} | Number of Q: {res['number_questions']}")
        print([x for x in res['questions']])
    else:
        print("Quizz has not been found")

if __name__ == '__main__':
    
    print("lol")
    #1
    #ping_server(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME)

    #2
    drop_collection(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME, mongodb_collectionname=MONGODB_COLLECTIONNAME)
    
    #3
    from data import quizes
    insert_many(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME, quiz_items=quizes)
    
    #4
    from data import prepare_quiz_to_insert
    quiz_item = prepare_quiz_to_insert("Quiz Viz", "Rtrqb-FgKCs", "single", 5, ["What are Bitcoins?", ["A type of physical currency","A digital currency","A loyalty program","An investment fund"], "What is one advantage of using Bitcoins?", ["High transaction fees","No need for a bank","Limited to large businesses","Requires a special wallet"], "Who can benefit from using Bitcoins?", ["Only large corporations","Freelancers and small businesses","Government agencies","Traditional banks"], "How are Bitcoins transferred?", ["Through bank transfers","Via postal service","Directly from person to person","Through mobile apps"], "What is a unique feature of Bitcoin transactions?", ["They are reversible","There are no chargebacks","They require a middleman","They have high fees"]])
    insert_one(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME, quiz_item=quiz_item)


    #5
    #get_quizzes(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME, mongodb_collectionname=MONGODB_COLLECTIONNAME)

    #6
    #criteria = {"name": "Quiz Viz"}
    #get_quiz(mongodb_uri=MONGODB_URI, mongodb_dbname=MONGODB_DBNAME, mongodb_collectionname=MONGODB_COLLECTIONNAME, criteria=criteria)
    