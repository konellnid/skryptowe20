#include "ZakupFileOpener.h"
#include <sstream>
#include <fstream>
#include <regex>

using namespace std;

const int NUMBER_OF_COLUMNS = 4;
const regex REGEX_DATE("\\d{2}\\.\\d{2}\\.\\d{4}");
const regex REGEX_DECIMAL("\\d+\\.?\\d*]?");
const regex REGEX_PRICE("\\d+\\.\\d{2}");

vector<vector<string>> getRowsFromZakupFile()
{
    const std::string FILE_NAME = "Zakup.txt";

    vector<vector<string>> rows;

    ifstream file(FILE_NAME);

    if (file.is_open())
    {
        string line;

        while (getline(file, line))
        {
            vector<string> singleRow = splitStringBySign(line, '\t');
            if (isRowInCorrectFormat(singleRow))
            {
                rows.push_back(singleRow);
            }
            else
            {
                file.close();

                rows.clear();
                return rows;
            }
        }
    }

    file.close();

    return rows;
}

bool isRowInCorrectFormat(vector<string> singleRow)
{
    if (singleRow.size() != NUMBER_OF_COLUMNS)
    {
        return false;
    }
    else
    {
        if (!regex_match(singleRow.front(), REGEX_DATE))
        {
            return false;
        }

        if (singleRow.at(1).length() == 0)
        {
            return false;
        }

        if (!regex_match(singleRow.at(2), REGEX_DECIMAL))
        {
            return false;
        }

        if (!regex_match(singleRow.at(3), REGEX_PRICE))
        {
            return false;
        }

        return true;
    }
}

vector<string> splitStringBySign(string stringToSplit, char sign)
{
    vector<string> splittedStringVector;

    stringstream ss(stringToSplit);
    string tmpValueHolder;

    while (getline(ss, tmpValueHolder, sign))
    {
        splittedStringVector.push_back(tmpValueHolder);
    }

    return splittedStringVector;
}
