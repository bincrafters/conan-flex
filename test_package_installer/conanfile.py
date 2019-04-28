#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile


class TestPackageConan(ConanFile):
    def test(self):
        self.run("flex --version", run_environment=True)
        self.run("flex %s" % os.path.join(self.source_folder, "basic_nr.l"), run_environment=True)
