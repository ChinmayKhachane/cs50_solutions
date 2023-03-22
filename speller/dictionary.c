// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <stdio.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
int word_count =0;
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *temp = table[index];
    while (temp != NULL)
    {
        if(strcasecmp(temp->word, word) == 0)
        {
            return true;
        }
    temp = temp->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
 int s = 0;
 for(int i =0; i<strlen(word); i++)
 {
    s += toupper(word[i]);
 }
return (s % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if(dict == NULL)
    {
        return false;
    }
    char word[LENGTH];
    while(fscanf(dict, "%s", word)!= EOF)
    {
        node *new = malloc(sizeof(node));
        if(new == NULL)
        {
            return false;
        }
        strcpy(new->word, word);
        new->next = NULL;

        int index = hash(word);
        if(table[index] == NULL)
        {
            table[index] = new;
        }
        else
        {
            new->next = table[index];
            table[index] = new;
        }
        word_count++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
for(int i = 0; i < N; i++)
{
    node *top = table[i];
    node *point = top;
    node *temp = point;

    while(point != NULL)
    {
        point = point->next;
        free(temp);
        temp = point;
    }
}
return true;
}
