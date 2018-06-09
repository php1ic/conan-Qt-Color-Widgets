import os
from conans import ConanFile, CMake, tools

class QtColorWidgetsConan(ConanFile):
    name = "Qt-Color-Widgets"
    version = "fbeaae4"
    license = "https://github.com/ess-dmsc/Qt-Color-Widgets/blob/master/COPYING"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Qt-Color-Widgets here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    # The temporary build diirectory
    build_dir = "./%s/build" % folder_name

    def source(self):
        self.run("git clone https://github.com/ess-dmsc/Qt-Color-Widgets.git")
        self.run("cd Qt-Color-Widgets && git checkout fbeaae4 && cd ..")

    def build(self):
        with tools.chdir(self.build_dir):
            cmake = CMake(self)
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            cmake.definitions["BUILD_STATIC_LIBS"] = "ON"
            cmake.definitions["QTCOLORWIDGETS_DESIGNER_PLUGIN"] = "OFF"
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = ""

            if tools.os_info.is_macos:
                cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"
                cmake.definitions["CMAKE_PREFIX_PATH"] = "/usr/local/opt/qt"
                cmake.definitions["CMAKE_SHARED_LINKER_FLAGS"] = "-headerpad_max_install_names"

            # cmake.configure(source_dir="..", build_dir=".")
            self.run("cmake --debug-output %s %s" % ("..", cmake.command_line))
            cmake.build(build_dir=".")
            os.system("make install DESTDIR=./install")

    def package(self):
        self.copy("*.h", dst="include", src="Qt-Color-Widgets/include")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["QtColorWidgets"]
