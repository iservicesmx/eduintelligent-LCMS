""" Interfaces for Faq """

from zope.interface import Interface

class IFaqFolder(Interface):
    """An Folder than contains Faq questions"""


class IFaqEntry(Interface):
    """An FAQ question"""
