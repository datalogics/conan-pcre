#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class PCREConan(ConanFile):
    name = "pcre"
    version = "8.41"
    url = "https://github.com/bincrafters/conan-pcre"
    homepage = "https://www.pcre.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Perl Compatible Regular Expressions"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "with_bzip2": [True, False]}
    default_options = ("shared=False", "with_bzip2=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    requires = "zlib/1.2.11@conan/stable"

    def source(self):
        source_url = "https://ftp.pcre.org"
        tools.get("{0}/pub/pcre/pcre-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.6@conan/stable")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PCRE_BUILD_TESTS"] = False
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            cmake.definitions["PCRE_STATIC_RUNTIME"] = not self.options.shared and "MT" in self.settings.compiler.runtime
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        cmake.patch_config_paths()
        self.copy(pattern="LICENCE", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
