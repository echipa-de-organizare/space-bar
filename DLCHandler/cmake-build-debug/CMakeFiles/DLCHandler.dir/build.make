# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\JetBrains\CLion 2021.2.2\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\JetBrains\CLion 2021.2.2\bin\cmake\win\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/DLCHandler.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/DLCHandler.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/DLCHandler.dir/flags.make

CMakeFiles/DLCHandler.dir/main.cpp.obj: CMakeFiles/DLCHandler.dir/flags.make
CMakeFiles/DLCHandler.dir/main.cpp.obj: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/DLCHandler.dir/main.cpp.obj"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\DLCHandler.dir\main.cpp.obj -c "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\main.cpp"

CMakeFiles/DLCHandler.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/DLCHandler.dir/main.cpp.i"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\main.cpp" > CMakeFiles\DLCHandler.dir\main.cpp.i

CMakeFiles/DLCHandler.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/DLCHandler.dir/main.cpp.s"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\main.cpp" -o CMakeFiles\DLCHandler.dir\main.cpp.s

# Object files for target DLCHandler
DLCHandler_OBJECTS = \
"CMakeFiles/DLCHandler.dir/main.cpp.obj"

# External object files for target DLCHandler
DLCHandler_EXTERNAL_OBJECTS =

DLCHandler.exe: CMakeFiles/DLCHandler.dir/main.cpp.obj
DLCHandler.exe: CMakeFiles/DLCHandler.dir/build.make
DLCHandler.exe: CMakeFiles/DLCHandler.dir/linklibs.rsp
DLCHandler.exe: CMakeFiles/DLCHandler.dir/objects1.rsp
DLCHandler.exe: CMakeFiles/DLCHandler.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable DLCHandler.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\DLCHandler.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/DLCHandler.dir/build: DLCHandler.exe
.PHONY : CMakeFiles/DLCHandler.dir/build

CMakeFiles/DLCHandler.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\DLCHandler.dir\cmake_clean.cmake
.PHONY : CMakeFiles/DLCHandler.dir/clean

CMakeFiles/DLCHandler.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler" "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler" "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug" "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug" "C:\Users\kidga\Desktop\Informatica\C++ Programming, CodeBlocks Projects\FiiCode 2022\space-bar\space-bar\DLCHandler\cmake-build-debug\CMakeFiles\DLCHandler.dir\DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/DLCHandler.dir/depend

