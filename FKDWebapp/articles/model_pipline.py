from sklearn.neighbors import KNeighborsClassifier
import pickle

CLASSIFIER = "articles/pickled/PassiveAggressive_model.sav"
TF_IDF = "articles/pickled/tfidf_fit.pkl"

SW = {
    "REAL":"Disagree",
    "FAKE":"Agree"
}

def getClassifier():
    with open(CLASSIFIER,'rb') as file:
        classifier = pickle.load(file)
    return classifier    

def tfidfTransformer():
    with open(TF_IDF,'rb') as file:
        tfidf = pickle.load(file)
    return tfidf

class ModelPipeline(object):
    def __init__(self,df_scrape,df_claim):
        self.df_claim = df_claim
        self.df_scrape = df_scrape

        self.tfidf = tfidfTransformer()
        self.classifier = getClassifier()

        self.scrape_article_body_tfidf = self.tfidf\
            .transform(self.df_scrape['body'].values)
        
        self.claim_article_body_tfidf = self.tfidf\
            .transform(self.df_claim['body'].values)
    
    def predict(self):
        predictions = self.classifier.predict(self.scrape_article_body_tfidf)
        knn = KNeighborsClassifier(n_neighbors=4)
        knn.fit(self.scrape_article_body_tfidf,predictions)
        parms = SW[knn.predict(self.claim_article_body_tfidf)[0]]
        prob = knn.predict_proba(self.claim_article_body_tfidf)[0][0]

        return [parms,prob]