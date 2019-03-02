import utils

BODY_KEY = "body"
STANCE_KEY = "stance"
HEADLINE_KEY = 'headline'

DATASET_FOLDER = utils.getFilePath('dataset',create=True)
PICKLED_FOLDER = 'pickled'

TRAIN_DATASET_FILES = {
    BODY_KEY: utils.getFilePath('dataset','train_bodies.csv'),
    STANCE_KEY:utils.getFilePath('dataset','train_stances.csv')
}
utils.checkRequiredFiles(TRAIN_DATASET_FILES)

TRAIN_DATASET_NUMPY = {    
    STANCE_KEY:utils.getFilePath(PICKLED_FOLDER,'train_stance_scipy.npy'),
    BODY_KEY:utils.getFilePath(PICKLED_FOLDER,'train_body_scipy.npy'),
    HEADLINE_KEY:utils.getFilePath(PICKLED_FOLDER,'train_headline_scipy.npy'),
}


TEST_DATASET_FILES = {
    BODY_KEY: utils.getFilePath('dataset','test_stances.csv'),
    STANCE_KEY:utils.getFilePath('dataset','competition_test_stances_label.csv'),
}

utils.checkRequiredFiles(TEST_DATASET_FILES)

TEST_DATASET_NUMPY = {
    STANCE_KEY:utils.getFilePath(PICKLED_FOLDER,'test_stance_scipy.npy'),
    BODY_KEY:utils.getFilePath(PICKLED_FOLDER,'test_body_scipy.npy'),
    HEADLINE_KEY:utils.getFilePath(PICKLED_FOLDER,'test_headline_scipy.npy'),
        
}

MERGE_TRAIN_FILE = utils.getFilePath(['dataset','final'],'final_stance_train.csv',create=True)
MERGE_TEST_FILE = utils.getFilePath(['dataset','final'],'final_stance_test.csv',create=True)