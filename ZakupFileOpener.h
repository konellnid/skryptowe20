#ifndef ZAKUP_FILE_OPENER_H
#define ZAKUP_FILE_OPENER_H

#include <string>
#include <vector>

std::vector<std::vector<std::string>> getRowsFromZakupFile();
bool isRowInCorrectFormat(std::vector<std::string> singleRow);
std::vector<std::string> splitStringBySign(std::string stringToSplit, char sign);

#endif
