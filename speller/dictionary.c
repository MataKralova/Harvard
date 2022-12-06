/**
 * Implements a dictionary's functionality.
 */
// Done by Mata

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// define trie structure
    typedef struct node
    {
        bool is_word;
        struct node *children[27];
    }
    node;

    node *root = NULL;

    // pointer to move along words letter by letter
    node *ptr = NULL;

    // pointer to dictionary file
    FILE *dic = NULL;

    // counter of words in dictiononary
    int counter;

    // bool release(struct node *ptr);
    void release(node *ptr);

/**
 * Returns true if word is in dictionary else false.
 */

bool check(const char *word)
{
    ptr = root;

    if (ptr == NULL)
    {
        printf("Null ptr!");
        return false;
    }

    int i;
    int n = strlen(word) + 1;
    int hash;

    for (i = 0; i < n; i++)
    {
        if (islower(word[i]))
        {
            // calculate hash index of given lowcase character
            hash = word[i] % 97;

            // if path doesn't exist, return false meaning misspelled, else move to next character
            if (ptr->children[hash] == NULL)
            {
                return false;
            }
            else
            {
                ptr = ptr->children[hash];
            }
        }
        else if (isupper(word[i]))
        {
            // calculate hash index of given upper case character
            hash = word[i] % 65;

            // if path doesn't exist, return false meaning misspelled, else move to next character
            if (ptr->children[hash] == NULL)
            {
                return false;
            }
            else
            {
                ptr = ptr->children[hash];
            }
        }
        else if (word[i] == '\'' && i > 0)
        {
            // calculate hash index of apostrophe
            hash = 26;

            // if path doesn't exist, return false meaning misspelled, else move to next character
            if (ptr->children[hash] == NULL)
            {
                return false;
            }
            else
            {
                ptr = ptr->children[hash];
            }
        }
        else
        {
            if (!ptr->is_word)
            {
                return false;
            }
        }
    }
    return true;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    root = malloc(sizeof(node));

    if (root == NULL)
    {
        fprintf(stderr, "Null pointer value.");
        return false;
    }

    // initialize boolean in the new node to FALSE
    root->is_word = false;

    // initialize all pointers in the new node to NULL
    for (int n = 0; n < 27; n++)
    {
        root->children[n] = NULL;
    }

    // open dictionary
    // char *dictionary = (argc == 3) ? argv[1] : DICTIONARY;
    FILE *dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        fprintf(stderr, "Could not open %s.", dictionary);
        return false;
    }

    // index of the children array
    int index = 0;

    // hash to know where to put letter in the trie
    int hash;

    // pointer to move along words letter by letter
    ptr = root;

    // load dictionary into memory one character at a time
    for (int c = fgetc(dic); c != EOF; c = fgetc(dic))
    {
        // for alphabetical characters (which are always lower case in dictionary))
        if (islower(c))
        {
            // hashing the letter to know where to put it in the trie
            hash = c % 97;

            // if path has not been created yet, create path
            if (ptr->children[hash] == NULL)
            {
                ptr->children[hash] = malloc(sizeof(node));
                ptr = ptr->children[hash];

                // initiate boolean in the new node to FALSE
                ptr->is_word = false;

                // initiate all pointers in the new node to NULL
                for (int n = 0; n < 27; n++)
                {
                    ptr->children[n] = NULL;
                }
            }
            else
            {
                ptr = ptr->children[hash];
            }

            index++;
        }

        // for apostrophes
        else if (c == '\'' && index > 0)
        {
            hash = 26;

            // if path has not been created yet, create path
            if (ptr->children[hash] == NULL)
            {
                ptr->children[hash] = malloc(sizeof(node));
                ptr = ptr->children[hash];

                // initiate boolean in the new node to FALSE
                ptr->is_word = false;

                // initiate all pointers in the new node to NULL
                for (int n = 0; n < 27; n++)
                {
                    ptr->children[n] = NULL;
                }
            }
            else
            {
                ptr = ptr->children[hash];
            }

            index++;
        }

        // if the end of the word is reached
        else
        {
            ptr->is_word = true;
            counter++;
            index = 0;
            ptr = root;
        }
    }

    fclose(dic);

    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return counter;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    ptr = root;

    if (root == NULL)
    {
        return false;
    }

    release(ptr);

    return true;
}

/**
 * Frees nodes that have all pointers NULL
 */

void release(node *ptr)
{
    // traverse the trie to the bottom
    for (int hash = 0; hash < 27; hash++)
    {
        if (ptr->children[hash] != NULL)
        {
            release(ptr->children[hash]);
        }
    }

    // free pointer to a node where all pointers are NULL
    free(ptr);
}