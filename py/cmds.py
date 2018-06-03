''' ComplexBear pubic API
'''
import db
import sys
import math
import json
import random
import os
import logging
from os import path


class Circle(object):
    def __init__(self, points, width):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.width = width
        xPoints, yPoints = zip(*points)
        self.xMax = max(*xPoints)
        self.xMin = min(*xPoints)
        self.yMax = max(*yPoints)
        self.yMin = min(*yPoints)
        self.points = points
        self.origin = ((self.xMax-self.xMin)/2 + self.xMin, (self.yMax-self.yMin)/2 + self.yMin)
        self.innerR = (self.yMax-self.yMin)/2 - self.width
        self.outerR = (self.yMax-self.yMin)/2 + self.width
        self.logger.debug('o%s, min(%s,%s), max(%s,%s)' %(self.origin, self.xMin,self.yMin, self.xMax,self.yMax))
        self.logger.info('Circle constructed')

    def validPoint(self, p):
        # is outside inner circle
        x, y = p
        r = math.sqrt( math.pow((x - self.origin[0]),2) + math.pow((y - self.origin[1]),2) )
        return r >= self.innerR and r <= self.outerR

    def validate(self):
        valid = True        
        for p in self.points:
            if not self.validPoint(p):
                valid = False
                break
        self.logger.info('circle valid? %s' %valid)
        return valid
    
    
    

    
    
class Cmd(object):

    TOKEN_PATH = '/var/www/tokens'
    
    def __init__(self, remotePort):
        self.port = remotePort
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, func, data):
        f = getattr(self, func)
        f(data)

    def loadContent(self, data):
        if self.validateToken(data):
            self.logger.info('loading blog js code from %s' %os.getcwd())
            with open('../js/blog.js','r') as f:
                return f.read()
            
    def storeToken(self):
        token = random.randint(0,100)
        with open(path.join(Cmd.TOKEN_PATH,'%s.token' %self.port),'w') as f:
            f.write('%s' %token)
        return token
    
    def validateToken(self, token):
        try:
            valid = False
            with open(path.join(Cmd.TOKEN_PATH,'%s.token' %self.port),'r') as f:
                refToken = f.read()
                valid = refToken == token
                self.logger.info('token %s is valid = %s' %(token, valid))
        except Exception, e:
            self.logger.exception(e)
        return token
        
    def authenticate(self, data):
        self.logger.info('authenticate')
        points = json.loads(data)
        self.logger.debug(points)
        circle = Circle(points, 40)
        valid = circle.validate()
        response = {'valid': valid}
        
        token = self.storeToken() if valid else 0
    
        response['token'] = token
        response['origin'] = circle.origin
        response['inner'] = circle.innerR
        response['outer'] = circle.outerR
        result = json.dumps(response)
        self.logger.debug(result)
        return result
