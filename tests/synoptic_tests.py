import unittest

from tests.settings import Settings
from util.gui import GuiUtils
from util.synoptic import SynopticUtils
from util.version import VersionUtils


class SynopticTests(unittest.TestCase):

    def __init__(self, methodName, synoptic=None):
        # Boilerplate so that unittest knows how to run these tests.
        super(SynopticTests, self).__init__(methodName)

        self.synoptic = synoptic

    def setUp(self):
        # Has to have an __init__ that accepts one argument for unittest's test loader to work properly.
        # However the config should never be the default (None) when actually running the tests.
        self.assertIsNotNone(self.synoptic)

        self.gui_utils = GuiUtils(Settings.gui_repo_path)
        self.synoptic_utils = SynopticUtils(Settings.config_repo_path)
        self.version_utils = VersionUtils(Settings.config_repo_path)

        if not self.version_utils.version_file_exists():
            self.skipTest("Can't determine which version of the GUI is being used.")

        self.gui_utils.get_gui_repo_at_release(self.version_utils.get_version())

    def test_GIVEN_synoptic_THEN_targets_that_it_defines_appear_in_opi_info(self):

        allowed_targets = self.gui_utils.get_valid_targets(self.gui_utils.get_opi_info_xml())

        try:
            type_target_pairs = self.synoptic_utils.get_type_target_pairs(self.synoptic_utils.get_xml(self.synoptic))
        except Exception as e:
            self.fail("In synoptic {}, XML failed to parse properly. Error text was: {}".format(self.synoptic, e))

        for type, target in type_target_pairs:
            if not self.synoptic_utils.target_should_be_ignored(target):
                self.assertIn(target, allowed_targets, "In synoptic {}, component target '{}' was unknown."
                              .format(self.synoptic, target))

    def test_GIVEN_synoptic_THEN_types_that_it_defines_appear_in_opi_info(self):

        allowed_types = self.gui_utils.get_valid_types(self.gui_utils.get_opi_info_xml())

        try:
            type_target_pairs = self.synoptic_utils.get_type_target_pairs(self.synoptic_utils.get_xml(self.synoptic))
        except Exception as e:
            self.fail("In synoptic {}, XML failed to parse properly. Error text was: {}".format(self.synoptic, e))

        for type, target in type_target_pairs:
            if not self.synoptic_utils.type_should_be_ignored(type):
                self.assertIn(type, allowed_types, "In synoptic {}, component type '{}' was unknown."
                              .format(self.synoptic, type))
