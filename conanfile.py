# -*- coding: utf-8 -*
from conans import ConanFile, tools, CMake


class NanaConan(ConanFile):
    name = "nana"
    license = "BSL-1.0"
    homepage = "http://nanapro.org"
    url = "https://github.com/cnjinhao/nana"
    description = "a modern C++ GUI library"
    author = "Jinhao"
    topics = ("nana", "gui-toolkit", "gui", "modern-cpp")
    exports = ("LICENSE")
    exports_sources = ("source/*", "build/*", "include/*", "extrlib/*", "CMakeLists.txt")
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "jpeg": [True, False],
        "png": [True, False],
        "filesystem": [True, False],
        "asound": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "jpeg": False,
        "png": False,
        "filesystem": False,
        "asound": False
    }

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires.add("freetype/2.9.1@bincrafters/stable")
            # FIXME: Can not find X11
            self.requires.add("xorgproto/2018.4@bincrafters/stable")
        if self.options.filesystem:
            self.requires.add("boost/1.69.0@conan/stable")
        if self.options.jpeg:
            self.requires.add("libjpeg/9c@bincrafters/stable")
        if self.options.png:
            self.requires.add("libpng/1.6.36@bincrafters/stable")
        if self.options.asound:
            # FIXME: Can not find libasound
            self.requires.add("libalsa/1.1.5@conan/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NANA_CMAKE_ENABLE_JPEG"] = self.options.jpeg
        cmake.definitions["NANA_CMAKE_FIND_BOOST_FILESYSTEM"] = self.options.filesystem
        cmake.definitions["NANA_CMAKE_ENABLE_PNG"] = self.options.png
        cmake.definitions["NANA_CMAKE_ENABLE_AUDIO"] = self.options.asound
        cmake.definitions["NANA_CMAKE_INSTALL"] = True
        cmake.configure(build_dir="build_subfolder")
        return cmake

    def build(self):
        tools.replace_in_file(file_path="CMakeLists.txt",
                              search="add_library(nana)",
                              replace="""include(conanbuildinfo.cmake)
                                 conan_basic_setup()
                                 add_library(nana)""")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
