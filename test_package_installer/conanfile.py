import os
from conans import ConanFile, tools


class TestPackageConan(ConanFile):
    def test(self):
        if not tools.cross_building(self.settings):
            self.run("flex --version", run_environment=True)
        self.run("flex %s" % os.path.join(self.source_folder, "basic_nr.l"), run_environment=True)
