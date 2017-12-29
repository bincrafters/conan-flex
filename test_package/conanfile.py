#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, RunEnvironment


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run("flex --version")
            self.run("flex %s" % os.path.join(self.source_folder, "basic_nr.l"))
