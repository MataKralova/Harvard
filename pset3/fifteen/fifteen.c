/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */

#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{

    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();

        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(50000);
        }

        // sleep thread for animation's sake
        usleep(50000);
    }

    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(200000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).
 */
// Done by Mata

 int i;
 int j;
 int n = 1;

void init(void)
{
    for(i = 0; i < d; i++)
    {
        for(j = 0; j < d; j++, n++)
        {
            board[i][j] = d*d - n;
        }
    }

    // swap 1 and 2 tiles if board dimension is even
    if(d % 2 == 0)
    {
        board[d - 1][d - 3] = 1;
        board[d - 1][d - 2] = 2;
    }
}

/**
 * Prints the board in its current state.
 */
// Done by Mata

void draw(void)
{
    for(i = 0; i < d; i++)
    {
        for(j = 0; j < d; j++)
        {
            if(board[i][j] == 0)
            {
                printf(" _ ");
            }
            else
            {
                printf("%2i ", board[i][j]);
            }
        }
        printf("\n");
    }
}


/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false.
 */
// Done by Mata

int a = 0;
int b = 0;
int holder1;
int holder2;
int x;
int y;
int blank;
int swap;

bool move(int tile)
{
    // if tile not on board
    if(tile == d * d || tile > d * d || tile < 0)
    {
        printf("Choose a tile from the board!");
        return false;
    }

    // blank = board[x][y];

    // set blank to bottom right corner location at the start
    if(swap == 0)
    {
        x = d - 1;
        y = d - 1;
        blank = board[x][y];
    }

    // find tile value on board and assign location [a],[b] to it
    for(i = 0; i < d; i++)
    {
        for(j = 0; j < d; j++)
        {
            if(board[i][j] == tile)
            {
                a = i;
                b = j;
            }
        }
    }

    // if blank is to the right of tile, move
    if(a == x && b == y - 1)
    {
        holder1 = a;
        holder2 = b;
        a = x;
        b = y;
        x = holder1;
        y = holder2;

    board[a][b] = tile;
    board[x][y] = blank;
    swap++;
    return true;
    }

    // if blank is to the left of tile, move
    else if(a == x && b == y + 1)
    {
        holder1 = a;
        holder2 = b;
        a = x;
        b = y;
        x = holder1;
        y = holder2;

    board[a][b] = tile;
    board[x][y] = blank;
    swap++;
    return true;
    }

    // if blank is below the tile, move
    else if(a == x - 1 && b == y)
    {
        holder1 = a;
        holder2 = b;
        a = x;
        b = y;
        x = holder1;
        y = holder2;

    board[a][b] = tile;
    board[x][y] = blank;
    swap++;
    return true;
    }

    // if blank is above the tile, move
    else if(a == x + 1 && b == y)
    {
        holder1 = a;
        holder2 = b;
        a = x;
        b = y;
        x = holder1;
        y = holder2;

    board[a][b] = tile;
    board[x][y] = blank;
    swap++;
    return true;
    }

    // if blank is not adjascent to tile
    else
    {
        return false;
    }
}

/**
 * Returns true if game is won (i.e., board is in winning configuration),
 * else false.
 */
// Done by Mata

bool won(void)
{
    int wrong = 0;
    n = 1;

    for(i = 0; i < d; i++)
    {
        for(j = 0; j < d; j++)
        {
            if(board[i][j] != n)
            {
                wrong++;
            }
            n++;
        }
    }

    if(board[d - 1][d - 1] == 0)
    {
        wrong--;
    }

    if(wrong == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
