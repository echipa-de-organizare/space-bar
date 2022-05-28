#include <iostream>
#include <fstream>
#include <map>
#include <windows.h>
#include <shlobj.h>

int next_planet_id = 0, current_state = 1;
std::map<int, std::string> planets;
std::map<int, std::string> working_directories;
CHAR documents[MAX_PATH];
HRESULT result = SHGetFolderPath(NULL, CSIDL_PERSONAL, NULL, SHGFP_TYPE_CURRENT, documents);
std::string path(documents), spacebarlogT(documents), spacebarlogP(documents), spacebarlogS(documents), spacebarlogL(
        documents), spacebarlogDLCD1(documents);
void handle_files()
{
    spacebarlogT += "\\spacebarlogT.txt";
    spacebarlogP += "\\spacebarlogP.txt";
    spacebarlogS += "\\spacebarlogS.txt";
    spacebarlogL += "\\spacebarlogL.txt";
    //time
    std::ifstream fin(spacebarlogT);
    if (!fin.good())
    {
        std::ofstream fout(spacebarlogT);
        fout << 0;
        fout.close();
    }

    //planet
    std::ifstream fin2(spacebarlogP);
    if (!fin2.good())
    {
        std::ofstream fout(spacebarlogP);
        fout << 1;
        fout.close();
    }
    //state
    std::ifstream fin3(spacebarlogS);
    if (!fin3.good())
    {
        std::ofstream fout(spacebarlogS);
        fout << 0;
        fout.close();
    }
    //location
    std::ifstream fin4(spacebarlogL);
    if (!fin4.good())
    {
//        std::cout << "lala";
        std::ofstream fout(spacebarlogL);
        fout << "0\n0";
        fout.close();
    }

}
void hardcode_planets()
{
    planets.insert(std::pair<int, std::string>(0, "Release Bar\\Bar\\Bar.exe"));
    planets.insert(std::pair<int, std::string>(1, "Release Travel\\Travel\\Travel.exe"));
    planets.insert(std::pair<int, std::string>(2, "Radio planet\\tcp-planet\\main.exe"));
    planets.insert(std::pair<int, std::string>(3, "End Planet\\Gadbuy\\main.exe"));
    planets.insert(std::pair<int, std::string>(4, "End Planet\\EndPlanet\\main.exe"));
    planets.insert(std::pair<int, std::string>(6, "EndCredits\\EndCredits.jar"));

    std::string empty;
    working_directories.insert(std::pair<int, std::string>(0, empty));
    working_directories.insert(std::pair<int, std::string>(1, empty));
    working_directories.insert(std::pair<int, std::string>(2, empty));
    working_directories.insert(std::pair<int, std::string>(3, empty));
    working_directories.insert(std::pair<int, std::string>(4, empty));
    working_directories.insert(std::pair<int, std::string>(6, empty));
}
/*
 * Blk — Today at 14:15
    -Verifica ce foldere sunt instalate
    -[OPTIONAL] Comunica cu coreul ca sa nu lase jocul sa ruleze si sa dea eroare daca lipseste vreun fisier esential (travel, bar, radio, etc)
    -"spacebarlogDLCT1" Creeaza/ia/muta un fisier text in care scrie despre DLC
        -TITLUL
        -Descrierea
        -minilista cu asseturi noi
    -Roxana o sa aiba de lucru in core sa gestioneze miscarea catre planetele noi
    -"spacebarlogDLCD1" Genereaza o planeta noua
       -numele planetei
       -IDul planetei
       -locatia
       -url catre poza
       -[]url catre executabil
    [optional] handlerul sa mute poza in documents
    -"spacebarlogDLCL" Fisier lista de DLCuri
    -Muta fisierul cu dialog nou
 * */
void add_dlc_planets()
{
    spacebarlogDLCD1 += "\\spacebarlogDLCD1.txt";
    std::ifstream fin(spacebarlogDLCD1);
    while (!fin.good())
    {
        fin.open(spacebarlogDLCD1);
    }
    if (fin.good())
    {
        std::string nume;
        std::string idstring;
        std::string locatie;
        std::string urlpoza;
        std::string urlexecutabil;

        std::getline(fin, nume);
        std::getline(fin, idstring);
        std::getline(fin, locatie);
        std::getline(fin, urlpoza);
        std::getline(fin, urlexecutabil);

        int id = atoi(idstring.c_str());
        planets.insert(std::pair<int, std::string>(id, urlexecutabil));
        std::string empty;
        working_directories.insert(std::pair<int, std::string>(id, empty));

        fin.close();
    }
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
    fout.open(spacebarlogT);
    fout << 0;
    fout.close();
}
int read_planet_id()
{
    int planet = -2;
    std::ifstream fin;
    fin.open(spacebarlogP);
    fin >> planet;
    fin.close();
    return planet;
}
int read_state()
{
    int state = -2;
    std::ifstream fin;
    fin.open(spacebarlogS);
    fin >> state;
    fin.close();
    return state;
}
void reset_planet_id()
{
    std::ifstream fin(spacebarlogP);
    if (fin.good())
    {
        std::ofstream fout(spacebarlogP);
        fout << 1;
        fout.close();
    }
}
void start_planet(int id)
{
    auto res = ShellExecute(nullptr, "open", get_planet_path(id).c_str(), nullptr, get_dir_path(id).c_str(),
                            SW_SHOWDEFAULT);
    std::cout << res << "\n";
//    STARTUPINFO si = { sizeof(STARTUPINFO) };
//    si.cb = sizeof(si);
//    si.dwFlags = STARTF_USESHOWWINDOW;
//    si.wShowWindow = SW_HIDE;
//    PROCESS_INFORMATION pi;
//    CreateProcess(get_planet_path(id).c_str(), NULL , NULL, NULL, FALSE, CREATE_NO_WINDOW , NULL, get_dir_path(id).c_str(), &si, &pi);
}
void run_handler()
{
    auto res = ShellExecute(nullptr, "open", "DLCHandler.exe", nullptr, "DLCHandler\\cmake-build-debug",
                            SW_SHOWDEFAULT);
    std::cout << res << "\n";
}
int main()
{
    //run core in background: either one of these lines
    //todo: remember to decomment
    ShowWindow(GetConsoleWindow(), SW_HIDE);
//    FreeConsole();

    handle_files();
//    int st = read_state();
//    if (st == 0)
    run_handler();
    hardcode_planets();
    add_dlc_planets();
    next_planet_id = read_planet_id();
    start_planet(next_planet_id);
    while (true)
    {
        int id = read_planet_id();
        int state = read_state();
        if (id == -1)
        {
            reset_planet_id();
            break;
        }
        if (state != 2)
            current_state = 1;
        if (next_planet_id != id)
        {
            next_planet_id = id;
            start_planet(next_planet_id);
        }
        else if (state == 2 && current_state == 1)
        {
            current_state = 2;
            start_planet(next_planet_id);
        }

    }
    return 0;

}
