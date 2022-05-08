#include <iostream>
#include <fstream>
#include <map>
#include <windows.h>
#include <chrono>

int next_planet_id = 0;
std::map<int, std::string> planets;
std::map<int, std::string> working_directories;
void hardcode_planets()
{
    planets.insert(std::pair<int, std::string>(0, "..\\..\\SpaceBar\\Bar.exe"));
    planets.insert(std::pair<int, std::string>(1, "..\\..\\Travel Environment\\Travel.exe"));
    planets.insert(std::pair<int, std::string>(2, "..\\..\\Radio planet\\tcp-planet\\main.exe"));
    planets.insert(std::pair<int, std::string>(3, "..\\..\\Planet\\planet.exe"));
    planets.insert(std::pair<int, std::string>(5, "..\\..\\Earth\\earth.exe"));
    planets.insert(std::pair<int, std::string>(6, "..\\..\\EndCredits\\EndCredits.jar"));

    std::string empty;
    working_directories.insert(std::pair<int, std::string>(0, empty));
    working_directories.insert(std::pair<int, std::string>(1, empty));
    working_directories.insert(std::pair<int, std::string>(2, "..\\..\\Radio planet\\tcp-planet"));
    working_directories.insert(std::pair<int, std::string>(3, "..\\..\\Planet"));
    working_directories.insert(std::pair<int, std::string>(5, "..\\..\\Earth"));
    working_directories.insert(std::pair<int, std::string>(6, empty));
}
std::string get_planet_path(int id)
{
    return planets[id];
}
std::string get_dir_path(int id)
{
    return working_directories[id];
}
void reset_time()
{
    std::ofstream fout;
    fout.open("../time_reset.txt");
    fout << 0;
    fout.close();
}
int read_planet_id()
{
    int planet = -2;
    std::ifstream fin;
    fin.open("../current_planet.txt");
    fin >> planet;
    fin.close();
    return planet;
}
void start_planet(int id)
{
    ShellExecute(nullptr, "open", get_planet_path(id).c_str(), nullptr, get_dir_path(id).c_str(), SW_SHOWDEFAULT);
}
int main()
{
    //run core in background: either one of these lines
//    ShowWindow (GetConsoleWindow(), SW_HIDE);
//    FreeConsole();
    hardcode_planets();
    next_planet_id = read_planet_id();
    reset_time();
    start_planet(next_planet_id);
    while (true)
    {
        int id = read_planet_id();
        if (id == -1)
        {
            std::cout << "lalal";
            break;
        }
        if (next_planet_id != id)
        {
            next_planet_id = id;
            start_planet(next_planet_id);
        }

    }
    return 0;
}
