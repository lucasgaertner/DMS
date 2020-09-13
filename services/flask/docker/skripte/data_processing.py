def normalize(data_path, file_name):


        import os
        import nltk
        #     print(os.getcwd())
        ##   print(os.listdir())
        #nltk.download("wordnet", data_path + "/" + "nltk")
        print(data_path, "LUCas:w")
        nltk.data.path.append(os.path.join(data_path ,"nltk"))
        from nltk.stem import WordNetLemmatizer
        import re


        tmp_list = []
        corpus = []
 
        print(data_path,file_name)
        file = open(os.path.join(data_path, file_name) + ".txt","r", encoding="latin-1")
       
        tmp_list.append(file.read())

        corpus.append(tmp_list)

        file.close()



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
                print(document)
                document = [stemmer.lemmatize(word) for word in document]
                document = ' '.join(document)

                documents.append(document)
        return documents
