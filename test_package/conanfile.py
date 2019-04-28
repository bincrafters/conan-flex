# -*- coding: utf-8 -*-

from conans import CMake, ConanFile, tools, RunEnvironment


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type",
    generators = 'cmake',

    def build_requirements(self):
        version = self.requires["flex"].ref.version
        user = self.requires["flex"].ref.user
        channel = self.requires["flex"].ref.channel

        self.build_requires("flex_installer/{}@{}/{}".format(version, user, channel))

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            with tools.environment_append(RunEnvironment(self).vars):
                cmake = CMake(self)
                cmake.test()
