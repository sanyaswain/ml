import argparse
import json
import os
import shutil
import subprocess
import tempfile
import unittest

from ast2vec.enry import install_enry


class EnryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gitdir = tempfile.mkdtemp()
        subprocess.check_call([
            "git", "clone", "-b", "develop",
            "https://github.com/src-d/ast2vec", cls.gitdir])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.gitdir)

    def test_install_enry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(output=tmpdir, tempdir=None)
            self.assertIsNone(install_enry(args))
            self._valivate_enry(tmpdir)

    def test_install_enry_no_args(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertIsNone(install_enry(
                target=os.path.join(tmpdir, "enry")))
            self._valivate_enry(tmpdir)

    def _valivate_enry(self, tmpdir):
        enry = os.path.join(tmpdir, "enry")
        self.assertTrue(os.path.isfile(enry))
        self.assertEqual(os.stat(enry).st_mode & 0o777, 0o777)
        output = subprocess.check_output([enry, self.gitdir, "--json"])
        files = json.loads(output.decode("utf-8"))
        self.assertIn("Python", files)


if __name__ == "__main__":
    unittest.main()