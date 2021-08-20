import pandas as pd
import sys

args=sys.argv

try:
    if len(args)!=4:
        print("Please ensure all files and size_filter are listed")
        print("python create_custom_dict.py <cui list file> <remove terms file> <size filter>")
        sys.exit()
    if not args[3].isnumeric():
        print("Enter an integer for size filter")
        sys.exit()

    cui_list = pd.read_csv(args[1], names=['cuis'])
    print('CUI list has been loaded')

    remove_terms = pd.read_csv(args[2], names=['term'])
    print('Remove term list has been loaded')
    size_filter = int(args[3])
    print("size filter", size_filter)
    dictionary = pd.read_csv("UMLS2019AB_9aug2021_size1_punct_stopwords_pattern_vid_aus.txt", sep="|")
    print("Global dictionary has been loaded\n\n")


except Exception as e:
    print(e)
    sys.exit()


cuis=cui_list['cuis'].to_list()
cuis=set(cuis)

dictionary = dictionary[dictionary['CUI'].str.contains('|'.join(cuis))]



remove_terms['term']= remove_terms['term'].str.lower()
remove_terms['term']= remove_terms['term'].str.strip()
print("Removing all occurances of the following terms from dictionary")
print(remove_terms,"\n\n")
rmv_terms=remove_terms['term'].to_list()
dictionary = dictionary[~dictionary["TERM"].isin(rmv_terms)]



if size_filter>1:
    print("removing all terms with size <=", size_filter)
    removed_terms = dictionary[dictionary['TERM'].apply(lambda x: len(str(x))<=size_filter)]
    print(removed_terms)
    print("The filtered out terms are saved as size_filter_removed_terms.csv\n\n")
    dictionary = dictionary[dictionary['TERM'].apply(lambda x: len(str(x))>size_filter)]
    removed_terms.to_csv("size_filter_removed_terms.csv", index=None, header=False)
else:
    if size_filter==1:
        print("size 1 terms has already been removed in global dictionary UMLS2019AB_9aug2021")
    print("No terms will be removed")



print("All terms with size <= 3 and terms of size 4 and 5 having multiple CUIs associated with them are considered potentially ambigious ")
print("saving potential ambigious terms as ambigious_terms.csv\n\n")
ambi_terms = dictionary[dictionary['NEW_CUI'].apply(lambda x: 'A' in x)]
print(ambi_terms.head())
print("Total ambigious terms",ambi_terms.shape,"\n\n")
ambi_terms.to_csv("ambigious_terms.csv", index=None)


print("Custom Dictionary")
print(dictionary)

print("Finished creating custom dictionary, saving..")
dictionary.to_csv("custom_dictionary_w_metadata.csv", index=None)
dictionary_trunc = dictionary[['TERM','NEW_CUI']]
term_tester = dictionary[['TERM','TERM']]
term_tester.to_csv("term_tester.txt", sep="|",index=None, header=False)
dictionary_trunc.to_csv("custom_dictionary_for_use.txt", sep="|",index=None, header=False)
print("Custom dictionary generation complete")
