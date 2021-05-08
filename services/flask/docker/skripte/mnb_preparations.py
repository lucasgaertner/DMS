import string
import re
import os 
def get_data(path):
    train_txt_dict = {}
    corpus = []
    path_list = os.listdir(path)
    try:
        path_list.remove("extracted")
        path_list.remove("extracted_text")
    except:
        pass
    for folder in path_list:
        train_txt_dict[folder] = {}
        for test_txt_docs in os.listdir(path + "/" + folder):
            tmp_list = []
            train_txt_dict[folder][test_txt_docs] = []
            train_txt_dict[folder][test_txt_docs].append(test_txt_docs)
            read_file = open(path + "/" + folder + "/" + test_txt_docs, "r")
            file_data = read_file.read()
            tmp_list.append(file_data)
            corpus.append(tmp_list)
            read_file.close()
    return corpus, train_txt_dict
    

def y_label(train_txt_dict):
    y_label_dict = {}
    y_label = []
    labelsigns = 1

    for key in train_txt_dict.keys():
        y_label_dict[key] = len(train_txt_dict[key])

    for key, values in y_label_dict.items():
        for label in range(values):
            y_label.append(labelsigns)
        labelsigns += 1
    return y_label


def normalize(corpus, data_path):
    import os
    import nltk
    print(os.getcwd())
    print(os.listdir())
    nltk.download("wordnet", os.path.join(data_path, "nltk"))
    nltk.data.path.append(data_path + "/nltk")
    from nltk.stem import WordNetLemmatizer
    import re
    documents = []
    stemmer = WordNetLemmatizer()

    for sen in range(0, len(corpus)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(corpus[sen]))  
	# remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document) 
	# Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
	# Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)
	# Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)
	# Converting to Lowercase
        document = document.lower()
	# Lemmatization
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)

        documents.append(document)
    return documents


