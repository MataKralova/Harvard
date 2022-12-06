#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    for (int j = 0; j < candidate_count; j++)
    {
        int success = 0;

        for (int k = 0; k < strlen(name); k++)
        {
            if (name[k] == candidates[j].name[k])
            {
                success++;
            }
        }
        if (success == strlen(name))
        {
            candidates[j].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    //winner count
    int w = 1;

    //set winner's votes to zero to allow comparison with candidate's votes
    candidate winners[MAX];
    winners[0].votes = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > winners[0].votes)
        {
            winners[0].name = candidates[i].name;
            winners[0].votes = candidates[i].votes;
            w = 1;
        }
        else if (candidates[i].votes == winners[0].votes)
        {
            winners[w].name = candidates[i].name;
            winners[w].votes = candidates[i].votes;
            w++;
        }
    }

    for (int j = 0; j < w; j++)
    {
        printf("%s\n", winners[j].name);
    }
    return;
}

