# NLP 2019 Custom Dictionary Generator
Generate a custom CUI dictionary for a Phenotype

## Requirements:
Python3, Pandas library, 2019AB UMLS Global dictionary

## Test Case
### `python create_custom_dict.py cui_list.txt remove_terms_list.txt 3`

cui_list.txt  - contains list of original CUIs selected for creating the custom dictionary. One CUI per line

remove_terms_list.txt - contains list of terms you want to remove from the dictionary. You can add stop words to this list. One term per line

3 - specifies the size filter, removes all terms <= char size 3

## Usage
### `python create_custom_dict.py <cui list file> <remove terms list> <filter size>`
