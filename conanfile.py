#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans.errors import ConanInvalidConfiguration
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class FlexConan(ConanFile):
    name = "flex"
    version = "2.6.4"
    url = "https://github.com/bincrafters/conan-flex"
    homepage = "https://github.com/westes/flex"
    description = "Flex, the fast lexical analyzer generator"
    topics = ("conan", "flex", "lex", "lexer", "lexical analyzer generator")
    license = "BSD-2-Clause"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports_sources = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {'shared': 'False'}

    def source(self):
        source_url = "https://github.com/westes/flex"
        tools.get("{0}/releases/download/v{1}/{2}-{3}.tar.gz".format(source_url, self.version,self.name, self.version),
                  sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("Flex is not supported on Windows.")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        configure_args = ['--prefix=%s' % self.package_folder]
        configure_args.append("--enable-shared" if self.options.shared else "--disable-shared")
        configure_args.append("--disable-static" if self.options.shared else "--enable-static")
        configure_args.append("--disable-nls")
        if str(self.settings.compiler) == "gcc" and float(str(self.settings.compiler.version)) >= 6:
            configure_args.append("ac_cv_func_reallocarray=no")
        with tools.chdir("sources"):
            if tools.cross_building(self.settings):
                # stage1flex must be built on native arch: https://github.com/westes/flex/issues/78
                self.run("./configure %s" % " ".join(configure_args))
                env_build.make(args=["-C", "src", "stage1flex"])
                self.run("mv src/stage1flex src/stage1flex.build")
                env_build.make(args=["distclean"])
                with tools.environment_append(env_build.vars):
                    env_build.configure(args=configure_args)
                    cpu_count_option = "-j%s" % tools.cpu_count()
                    self.run("make -C src %s || true" % cpu_count_option)
                    self.run("mv src/stage1flex.build src/stage1flex")
                    self.run("touch src/stage1flex")
                    env_build.make(args=["-C", "src"])
            else:
                with tools.environment_append(env_build.vars):
                    env_build.configure(args=configure_args)
                    env_build.make()
            env_build.make(args=["install"])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="COPYING", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
