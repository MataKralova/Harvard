#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        int success = 0;

        // Check that the voted name matches a candidate name
        for (int j = 0; j < strlen(name); j++)
        {
            if (name[j] == candidates[i][j])
            {
                success++;
            }
            else
            {
                break;
            }
        }

        // If the whole name matches, record the vote
        if (success == strlen(name))
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    // Placeholder for sorting
    int a = 0;
    int b = 0;

    // Counter to indicate sort finished
    int swap;

    do
    {
        swap = 0;

        for (int i = 0; i < pair_count - 1; i++)
        {
            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[i + 1].winner][pairs[i + 1].loser])
            {
                a = pairs[i].winner;
                b = pairs[i].loser;
                pairs[i].winner = pairs[i + 1].winner;
                pairs[i].loser = pairs[i + 1].loser;
                pairs[i + 1].winner = a;
                pairs[i + 1].loser = b;
                swap++;
            }
        }
    }
    while (swap != 0);
    return;
}

// Find circle
bool find_circle(int w, int l)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[l][i] == true)
        {
            if (w == i)     // Circle found
            {
                return true;
            }
            if (find_circle(w, i)) // using 2nd n instead of l will shift winner and loser pair one step along the chain
            {
                return true;
            }
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    // Treat each pair
    for (int i = 0; i < pair_count; i++)
    {
        // store current winner and current loser indexes
        int w = pairs[i].winner;
        int l = pairs[i].loser;
        //int n = 0;

        if (!find_circle(w, l))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Find circle
//bool find_circle(int n, int w, int l)
//{
//    for (n = 0; n < candidate_count; n++)
//    {
//        if (locked[l][n] == true)
//        {
//            if (w == n)     // Circle found
//            {
//                return true;
//            }
//            if (find_circle(n, w, n)) // using 2nd n instead of l will shift winner and loser pair one step along the chain
//            {
//                return true;
//            }
//        }
//    }
//    return false;
//}







// Print the winner of the election
void print_winner(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        bool loser = false;

        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == true)
            {
                loser = true;
                break;
            }
        }
        if (!loser)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}

