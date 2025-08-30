using System;
using System.Collections.Generic;

public class Map
{
    public bool[][] map = new bool[5][]
    {
        [false, false, false, false, false],
        [false, false, false, false, false],
        [false, false, false, false, false],
        [false, false, false, false, false],
        [false, false, false, false, false]
    };

    public char BoolToChar(bool boolean)
    {
        if (boolean)
        {
            return 'O';
        }
        else
        {
            return 'X';
        }
    }

    public void LogMap(bool[][] map)
    {
        foreach (bool[] list in map)
        {
            foreach (bool boolean in list)
            {
                Console.Write(BoolToChar(boolean));
            }
            Console.Write("\n");
        }
    }
}