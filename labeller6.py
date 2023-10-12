import json
import pandas as pd
import csv
import os

# save the unlabelled data into a dataframe
path = '/Users/alexanderciechonski/Desktop/Reddit_copy/saas2.json'
with open(path, 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df.drop_duplicates()

def check_classes(name,l): # check a specific class name in the classes list
    for i in l:
        if i[1] == str(name):
            return True
    return False

def print_data(index): # print a specific datapoint in the unlabelled data
    title = df['title'][index]
    content = df['content'][index]
    print(title)
    print(content)

def print_classes(li): # print all classes in separate rows
    print("Available classes:")
    for cl in li: 
        print(cl)  

def initializie_file(filepath): # establish the columns in a csv file
    cols = 'index,class'
    with open(filepath, 'r+') as file:
        file_content = file.read()
        if len(file_content) == 0:
            file.write(cols + '\n')

def find_starting_index(filepath): # find the index at which data to be labelled starts
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        max_index = 0
        for row in csv_reader:
            index = int(row['index'])
            if index > max_index:
                max_index = index
    return max_index

def update_classes(filepath): # update the classes list with classes already established in the file
    if os.path.getsize(filepath) == 0:
        class_list = []
        return class_list
    else:
        df = pd.read_csv(filepath)
        class_list = df['class'].tolist()
        updated_list = list(set(class_list))
        numbered_list = [(i, updated_list[i]) for i in range(len(updated_list))]
    return numbered_list

def merge(class1, class2, updated_name, file_path): # merge two classes together
    df = pd.read_csv(file_path)
    df['class'] = df['class'].replace([class1, class2], updated_name)
    df.to_csv(file_path, index=False)

def rename(old_name, new_name, filepath): # rename a class
    df = pd.read_csv(filepath)
    data = df['class']
    new_df = data.replace(old_name, new_name)
    df.to_csv(filepath, index = False)

def classify(i, name, classes, filepath): # label a specific datapoint
    if not check_classes(name, classes):
        num_classes = len(classes) + 1
        dp = (num_classes, name)
        classes.append(dp)
    with open(filepath, 'a') as file:
        file.write(f'{i},{name}\n')

def main():
    filepath = 'labelled_data8.csv'
    initializie_file(filepath)
    i = find_starting_index(filepath)

    while i < len(df):
        classes = update_classes(filepath) 
        print_data(i) 
        print_classes(classes) 
        user_input = input('enter class:').lower()
        if user_input == 'exit':
            break
        elif user_input == 'next':
            i += 1
        elif user_input == 'prev':
            i -= 1
        elif user_input == 'merge':
            loop1 = True
            while loop1: # check if the enterred class name is valid
                class1 = input('enter the 1st class you want to merge:')
                if check_classes(class1, classes):
                    loop = False
                else:
                    class1 = input("The specified class does not exist. Please try again.")
            loop2 = True
            while loop2: # check if the enterred class name is valid
                class2 = input('enter the 2nd class you want to merge:')
                if check_classes(class2, classes):
                    loop2 = False
                else:
                    class2 = input("The specified class does not exist. Please try again.")
            updated_name = input('enter the new class name:')
            merge(class1, class2, updated_name, filepath)
        elif user_input == 'rename':
            loop = True
            while loop: # check if the enterred class name is valid
                old_name = input('select a class you want to rename:')
                if check_classes(old_name, classes):
                    loop = False
                else:
                    old_name = input("The specified class does not exist. Please try again.")
            new_name = input('what would you like to rename it:')
            rename(old_name, new_name, filepath)
        else:
            new_name = user_input
            classify(i, new_name, classes, filepath)
            i += 1
main()