# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import ISecuritySchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class SecurityRegistryIntegrationTest(unittest.TestCase):
    """Test that the security settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(ISecuritySchema)

    def test_security_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="security-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('plone.app.registry' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_enable_self_reg_setting(self):
        self.assertTrue('enable_self_reg' in ISecuritySchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISecuritySchema.enable_self_reg'],
            False)

    def test_enable_user_pwd_choice_setting(self):
        self.assertTrue('enable_user_pwd_choice' in ISecuritySchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISecuritySchema.enable_user_pwd_choice'],
            False)

    def test_enable_user_folders_setting(self):
        self.assertTrue('enable_user_folders' in ISecuritySchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISecuritySchema.enable_user_folders'],
            False)

    def test_allow_anon_views_about_setting(self):
        self.assertTrue('allow_anon_views_about' in ISecuritySchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISecuritySchema.allow_anon_views_about'],
            False)

    def test_use_email_as_login_setting(self):
        self.assertTrue('use_email_as_login' in ISecuritySchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISecuritySchema.use_email_as_login'],
            False)


class SecurityControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the security control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

    def test_security_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Security').click()

    def test_security_control_panel_backlink(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_security_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_enable_self_reg(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getControl('Enable self-registration').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema)
        self.assertEqual(settings.enable_self_reg, True)

    def test_enable_user_pwd_choice(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Let users select their own passwords').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema)
        self.assertEqual(settings.enable_user_pwd_choice, True)

    def test_enable_user_folders(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Enable User Folders').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema)
        self.assertEqual(settings.enable_user_folders, True)

    def test_allow_anon_views_about(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getControl(
            "Allow anyone to view 'about' information").selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema)
        self.assertEqual(settings.allow_anon_views_about, True)

    def test_use_email_as_login(self):
        self.browser.open(
            "%s/@@security-controlpanel" % self.portal_url)
        self.browser.getControl(
            "Use email address as login name").selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema)
        self.assertEqual(settings.use_email_as_login, True)
