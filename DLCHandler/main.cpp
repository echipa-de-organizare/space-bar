#include  <bits/stdc++.h>
#include <fstream>
#include <windows.h>
#include <winbase.h>
#include <shlobj.h>
#include <string>
#include <dirent.h>

#define STARTING_PLANET_ID 7
#define MAX_NUMBER_OF_DLCS 10

const char SIGNATURE[] = "75 6e 76 2d 66 6e 2d 76 67 76 2d 6e 65 6e 67 6e 7a 2d "
                         "62 2d 66 70 75 72 7a 6e 2d 70 68 7a 2d 66 6e 2d 76 67 "
                         "76 2d 6f 6e 74 76 2d 71 65 62 74 68 79 2d 76 61 2d 69 "
                         "72 61 6e";
char DLC_FOLDER_PATH[] = "..\\..\\DLCs";


CHAR documents[MAX_PATH];
bool authorizedDLC[MAX_NUMBER_OF_DLCS];

int getNumberOfDLCs() {
    char *path = DLC_FOLDER_PATH;
    struct dirent *entry;
    DIR *dp;

    dp = opendir(path);
    if (dp == nullptr) {
        perror("opendir: Path does not exist or could not be read.");
        return -1;
    }

    int number = -2;
    while ((entry = readdir(dp))) {
        char dirPath[MAX_PATH];
        strcpy(dirPath, path);
        strcat(dirPath, "\\");
        strcat(dirPath, entry->d_name);
        ++number;
    }

    closedir(dp);
    return number;
}

std::string getSignatureFilePath(char *path, int position) {
    struct dirent *entry;
    DIR *dp;

    dp = opendir(path);
    if (dp == nullptr) {
        perror("opendir: Path does not exist or could not be read.");
        return "";
    }

    std::string toReturn;
    int numberOfFolder = -1;
    while ((entry = readdir(dp))) {
        if (numberOfFolder == position) {
            toReturn = path;
            std::string folderName = entry->d_name;
            toReturn += "\\" + folderName + "\\signature.sbdlc";
            break;
        }
        ++numberOfFolder;
    }

    closedir(dp);
    return toReturn;
}

int checkDLCs() {
    std::string signatureFilePath, readSignature;
    int numberOfFolders = getNumberOfDLCs();
    int realNumber = 0;
    for (int i = 1; i <= numberOfFolders; ++i) {
        signatureFilePath = getSignatureFilePath(DLC_FOLDER_PATH, i);

        if (signatureFilePath.empty()) {
            authorizedDLC[i] = false;
            continue;
        }

        std::ifstream fin(signatureFilePath);
        std::getline(fin, readSignature);
        fin.close();

        if (readSignature != SIGNATURE) {
            authorizedDLC[i] = false;
            continue;
        }
        authorizedDLC[i] = true;
        ++realNumber;
    }
    return realNumber;
}

std::string getDetailFilePath(char *path, int position) {
    struct dirent *entry;
    DIR *dp;

    dp = opendir(path);
    if (dp == nullptr) {
        perror("opendir: Path does not exist or could not be read.");
        return "";
    }

    std::string toReturn;
    int numberOfFolder = -1;
    while ((entry = readdir(dp))) {
        if (numberOfFolder == position) {
            toReturn = path;
            std::string folderName = entry->d_name;
            toReturn += "\\" + folderName + "\\DLCDescription.sbdlc";
            break;
        }
        ++numberOfFolder;
    }

    closedir(dp);
    return toReturn;
}

std::string getPlanetPath(char *path, int position) {
    struct dirent *entry;
    DIR *dp;

    dp = opendir(path);
    if (dp == nullptr) {
        perror("opendir: Path does not exist or could not be read.");
        return "";
    }

    std::string toReturn;
    int numberOfFolder = -1;
    while ((entry = readdir(dp))) {
        if (numberOfFolder == position) {
            toReturn = path;
            std::string folderName = entry->d_name;
            toReturn += "\\" + folderName + "\\Planet";
            break;
        }
        ++numberOfFolder;
    }

    closedir(dp);
    return toReturn;
}

void copyDLCDetails(int numberOfDLCs) {
    std::string detailFilePath, spacebarlogDLCT;
    for (int i = 1; i <= numberOfDLCs; ++i) {
        if (authorizedDLC[i]) {
            detailFilePath = getDetailFilePath(DLC_FOLDER_PATH, i);
            spacebarlogDLCT = documents;
            spacebarlogDLCT += "\\spacebarlogDLCT" + std::to_string(i) + ".txt";

            if (!detailFilePath.empty()) {
                if (!CopyFileA(detailFilePath.c_str(), spacebarlogDLCT.c_str(), false)) {
                    perror("No Details found");
                }
            }
        }
    }
}

std::string movePlanetIcon(const std::string& planetIconPath, const std::string& planetName) {
    std::string newPath(documents);
    newPath += "\\" + planetName + ".png";
    if (!CopyFileA(planetIconPath.c_str(), newPath.c_str(), false)) {
        return "No icon found";
    }
    return newPath;
}

void printDLCList(int numberOfDLCs, bool planetCorrectlyGenerated[]) {
    std::string planetPath, spacebarlogDLCL;
    spacebarlogDLCL = documents;
    spacebarlogDLCL += "\\spacebarlogDLCL.txt";

    std::queue<std::string> states;

    std::ifstream fin(spacebarlogDLCL);
    if (fin.good()) {
        int lineNumber = 1;
        std::string line;
        while (std::getline(fin, line)) {
            if (lineNumber % 2 && lineNumber != 1) {
                states.push(line);
            }
            ++lineNumber;
        }
    }

    std::ofstream fout(spacebarlogDLCL);
    fout << numberOfDLCs << "\n";

    for (int i = 1; i <= numberOfDLCs; ++i) {
        if (authorizedDLC[i] && planetCorrectlyGenerated[i]) {
            planetPath = getPlanetPath(DLC_FOLDER_PATH, i);
            std::string planetName;
            std::string planetNamePath;

            planetNamePath = planetPath + "\\PlanetName.sbdlc";

            if (!planetNamePath.empty()) {
                std::ifstream fin(planetNamePath);
                std::getline(fin, planetName);
                fin.close();
            } else {
                perror("Oh my god the planet name file wasn't there\n");
                planetCorrectlyGenerated[i] = false;
            }
            fout << planetName << "\n";
            if (states.empty()) {
                fout << "0\n";
            } else {
                fout << states.front() << "\n";
                states.pop();
            }
        }
    }

    fout.close();
}

void generatePlanets(int numberOfDLCs, int startingID) {
    std::string planetPath, spacebarlogDLCD;
    int planetID = startingID;
    struct location {
        int x;
        int y;
    };

    bool planetCorrectlyGenerated[numberOfDLCs + 1];
    for (int i = 1; i <= numberOfDLCs; ++i) {
        if (authorizedDLC[i]) {
            planetPath = getPlanetPath(DLC_FOLDER_PATH, i);
            spacebarlogDLCD = documents;
            spacebarlogDLCD += "\\spacebarlogDLCD" + std::to_string(i) + ".txt";

            planetCorrectlyGenerated[i] = true;
            std::string planetName;
            std::string planetExePath;
            std::string planetNamePath;
            std::string planetIconPath;
            std::string locationPath;

            locationPath = planetPath + "\\Location.sbdlc";
            planetNamePath = planetPath + "\\PlanetName.sbdlc";

            struct location location = {0, 0};

            if (!locationPath.empty()) {
                std::ifstream fin(locationPath);
                fin >> location.x;
                fin >> location.y;
                fin.close();
            } else {
                perror("Oh my god the location file wasn't there\n");
                planetCorrectlyGenerated[i] = false;
            }


            if (!planetNamePath.empty()) {
                std::ifstream fin(planetNamePath);
                std::getline(fin, planetName);
                fin.close();
            } else {
                perror("Oh my god the planet name file wasn't there\n");
                planetCorrectlyGenerated[i] = false;
            }


            planetIconPath = planetPath + "\\" + planetName + ".png";
            planetExePath = planetPath + "\\" + planetName + ".exe";

            std::ofstream fout(spacebarlogDLCD);
            fout << planetName << "\n";
            fout << planetID << "\n";
            fout << location.x << " " << location.y << "\n";

            if (movePlanetIcon(planetIconPath, planetName) == "No icon found") {
                planetCorrectlyGenerated[i] = false;
            } else {
                fout << movePlanetIcon(planetIconPath, planetName) << "\n";
            }

            fout << planetExePath << "\n";
            fout.close();

            planetID++;
        }
    }

    printDLCList(numberOfDLCs, planetCorrectlyGenerated);
}

void moveXML(int numberOfDLCs)
{
    std::string destinationPath, planetPath, sourcePath;
    destinationPath = "..\\..\\Resources\\resourcesradio\\ArtifactD.xml";
    for (int i = 1; i <= numberOfDLCs; ++i) {
        if (authorizedDLC[i]) {
            planetPath = getPlanetPath(DLC_FOLDER_PATH, i);
            sourcePath = planetPath + "\\ArtifactD.xml";
            if (!CopyFileA(sourcePath.c_str(), destinationPath.c_str(), FALSE) ) {
                perror("Could not copy XML");
            }
        }
    }
}

int main() {
    ShowWindow(GetConsoleWindow(), SW_HIDE);
    SHGetFolderPathA(nullptr, CSIDL_PERSONAL, NULL, 0, documents);

    int numberOfDLCs = checkDLCs();
    copyDLCDetails(numberOfDLCs);
    generatePlanets(numberOfDLCs, STARTING_PLANET_ID);
    moveXML(numberOfDLCs);
    return 0;
}
