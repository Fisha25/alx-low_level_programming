#include "main.h"

/**
 * more_numbers - a function that prints 10 times the numbers, from 0 to 14
 * using  _putchar only 3 times
 * Return: 0-14 x10 followed by new line
 */
void more_numbers(void)
{
int i, row;

for (row = 0; row < 10; row++)
	{
for (i = 0; i <= 14; i++)
{
if (i >= 10)
{
_putchar((i / 10) + '0');
}
_putchar((i % 10) + '0');
}
_putchar('\n');
}
}
