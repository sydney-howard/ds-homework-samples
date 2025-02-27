#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:41:14 2024
@author: sydney howard
DS2000 Programming With Data
hw6.py
Homework 6, All tasks
This program defines the functions and executes the code outlined in Homework 6. 

Question 1:
I think the theme of this book is something to do with family and being a woman. The second most used word is "little" used 234 times and "child" is used 177 times. This leads me to think someone has a child, or a young child is extremely relevant to the story. The words "life" and "man" support my notion of a family. I believe this is about womanhood due to the usage of the words "woman" 82 times and "mother" 182 times. 
"""
# Import
import matplotlib.pyplot as plt

# Defining Functions

# Function 1
def clean_word(word): # Takes in a word and returns it 'cleaned' in all lowercase and alphabet.
    cleaned_word = ''
    for letter in word.strip().lower(): # Checks each letter to make sure it's alphabetical.
        if letter.isalpha(): 
            cleaned_word += letter
    return cleaned_word # Returns cleaned word.
       
# Function 2 
def clean_list(words_list): # Takes a list of words and 'cleans' them.
    cleaned_word_list = []
    for word in words_list: # Reiterates the clean_word() function for all words in the given list.
        cleaned = clean_word(word)
        if cleaned == "": # Does not include empty strings.
            continue
        else:
            cleaned_word_list.append(cleaned) # Adds cleaned words to a new list.
    return sorted(cleaned_word_list) # Returns a new list of cleaned words.

# Function 3
def remove_boring_words_from_list(main_list, boring_list): # Removes 'boring words' from a list of words.
    interesting_list = []
    for word in main_list: # Repeats the loop for every word in the given list.
        if word in boring_list: # Only adds the word to the new 'interesting' list if it does not appear on the boring list.
            continue
        else:
           interesting_list.append(word)
    return interesting_list # Returns a new list of words without the 'boring' words.

# Function 4
def read_words_from_file(filename): # Reads a file and creates a list of strings with every word in the file.
    words_list = []
    with open(filename, 'r') as file:
        for line in file: # Repeats the loop for every line in the file.
            words = line.split()  # Splits each line into words by spaces.
            for word in words: # Repeats for every word in the line.
                words_list.append(word)  # Append each word individually to the list
    return words_list # Returns a list of strings (words) from the whole file.

# Function 5
def read_novel(filename, boring_list): # Combines functions 1-4 to read a novel (.txt file) into a list of strings, cleans the list of words, and removes boring words.
    novel_words = read_words_from_file(filename) # Stores a list of words from a file. 
    clean_novel_words = clean_list(novel_words) # Cleans the list of words stored.
    return remove_boring_words_from_list(clean_novel_words, boring_list) # Retuns a list of words from a novel, cleaned, without boring words.

# Function 6
def unique_words(words_list): # Creates a new list of words without repitition from a list of words.
    unique_list = []
    for word in words_list: # Repeats the loop for every word in the given list.
        if word in unique_list: # If the word is already in the new list, do not add it.
            continue
        else: 
            unique_list.append(word)
    return unique_list # Returns a new list of only unique words from the given list.
        
# Function 7
def get_word_frequencies(main_list): # Counts the number of times a word is used in a file, and returns a tuple with the (count, word) in descending order.
    unique_words_list = unique_words(main_list) # Calls function 6 and gets a list of unique words from the file.
    frequency_with_word_list = []
    for word in unique_words_list: # Repeaats the loop for every word in the unique words list.
        if word in unique_words_list: # If the word is in the unique words list, count the number of occurances in the main given list.
            count = main_list.count(word)
        tuple_count = (count, word) # Creates a tuple for every unique word with its frequency and what the word is.
        frequency_with_word_list.append(tuple_count) # Creates a list of the tuples.
    sorted_frequencies = sorted(frequency_with_word_list, reverse = True) # Sorts the tuples from most frequent to least frequent.
    return sorted_frequencies # Returns a list of descending tuples with (word frequency, word).

# Function 8
def read_all_novels(boring_list): # Takes the 'books.txt' file and makes a list, then reads all of the book files mentioned and stores a list of words from each book in a big list.
    books_list = []
    all_novels_list = []
    with open("books.txt", 'r') as file:
        for book in file: # For each book title in the file, add it to the list of files.
            books_list.append(book.strip())
    for book in books_list: # For each book in the list of files, read ut with function 5 and add the returned lists of words to another list.
        novel_words = read_novel(book, boring_list)
        all_novels_list.append(novel_words)
    return all_novels_list # Returns a list of lists of cleaned, non-boring words from each book.

# Function 9
def calculate_theme_score(book_words, theme_words): # Calculates the theme score of a book by taking in a list of book words and a list of themed words.
    theme_occurances = 0 # Defines the variable 
    for word in book_words: # Repeats the loop for every word in the given list
        if word in theme_words: # If the word is in the list of theme words, add +1 to the score.
            theme_occurances = theme_occurances + 1
    book_word_count = len(book_words) # Counts the total number of words in the book.
    theme_score = (theme_occurances * 1000) / book_word_count # Calculates the theme score using the given equation.
    return theme_score # Returns the theme score.

# Function 10
def get_theme_scores(many_books_words, theme_words): # Calculates many theme scores by using function 9 and taking in a list of words.
    theme_scores = []
    for book in many_books_words: # Calculates the theme score for each book in the list of lists, and then makes a list of the scores.
        one_score = calculate_theme_score(book, theme_words)
        theme_scores.append(one_score)
    return theme_scores # Returns a list of theme scores for each book.

# Function 11
def visualize_themes(romance_scores, adventure_scores, titles): # Creates a plot of each theme score and thier corresponding titles.
    plt.figure(figsize=(6, 4), dpi=250)
    plt.xlabel("Romance Scale") # Romance scale on the X axis.
    plt.ylabel("Adventure Scale") # Adventure scale on the Y axis.
    plt.title("A Few Classics Mapped on Themes") # Title
    colors = ["green", "pink", "red", "blue", "purple"] # List of colors for each point.
    plt.scatter(romance_scores, adventure_scores, marker = "x", color = colors) # Plots each score
    for i in range(len(romance_scores)): # Plots each title at each score 
        plt.text(romance_scores[i] + .1, adventure_scores[i], titles[i], fontsize = 10) # The '+.1' ensures no overlap of the point and the title.
    plt.savefig("hw6.png", bbox_inches="tight") # Saves plot
    plt.show()  # Displays plot
        
# Function 12 Main Function
def main(): 
    boring_words = read_words_from_file("stop_words.txt") # Reads 'stop_words.txt' using function 4 and stores it as boring words.
# Code from main 1
#   scarlet_letter_novel = read_novel("TheScarletLetter.txt", boring_words)
#   scarlet_letter_frequencies = get_word_frequencies(scarlet_letter_novel)
#   print(scarlet_letter_frequencies[0:30])
    all_books_words = read_all_novels(boring_words) # Stores list of lists of all words from the novels, without the boring words from the 'stop_words.txt' file.
    romance_words = ["heart", "love", "desire", "sweet", "marry"] # Defines romance words.
    adventure_words = ["road", "run", "trouble", "gun", "boat"] # Defines adventure words.
    romance_scores = get_theme_scores(all_books_words, romance_words) # Calculates romance scores for all books.
    adventure_scores = get_theme_scores(all_books_words, adventure_words) # Calculates the adventure scores for all books.
    titles = ["Tale Of Two Cities", "Huckleberry Finn", "The Scarlett Letter", "Kim", "Treasure Island"] # List of the titles of all books (in the same order as the scores)
    visualize_themes(romance_scores, adventure_scores, titles) # Creates the plot.
    
    
# Calling Main
main()