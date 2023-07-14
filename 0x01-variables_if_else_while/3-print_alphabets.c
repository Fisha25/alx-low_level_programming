#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>
/**
 * main - Entry point
 *
 * Return: Always 0 (Success)
 */
int main(void)
{
	int low;

	for (low = 'a'; low <= 'z'; low++)
	{
		low=tolower(low);
		putchar(low);
	for (low = 'A'; low <= 'Z'; low++)
	
	{	
	       	low=tolower(low);
		putchar(low);
		break;
}
}
putchar('\n');

	return (0);
}

