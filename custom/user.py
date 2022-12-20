# -*- coding: utf-8 -*-
class User(object):
    def __init__(self, id, office, name):
        self.id = id
        self.office = office
        self.name = name

    def __str__(self):
        return '<User>: {} : {} ({}, {})'.format(self.id, self.office, self.name)

    def __repr__(self):
        return '<User>: {} : {} ({}, {})'.format(self.id, self.office, self.name)