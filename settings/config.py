"""
Configuration file
All settings are stored here
"""

LOG_FILE_NAME = 'log'
LOG_MAX_SIZE_BYTES = 1024 * 1024  # MB

PROXY_PROTOCOL = 'http'
PROXY_SOCKS = 'http'
PROXY_ADDRESS = '177.136.122.98'
PROXY_PORT = '53281'

REGISTERED_COURSES = {'BS1':    ['1', '2', '3', '4', '5', '6'],
                      'BS2':    ['1', '2', '3', '8', '5', '6', '7'],
                      'BS3':    ['SE', 'RO', 'DS1', 'DS2'],
                      'BS4':    ['SE', 'RO', 'DS'],
                      'M-SE':   ['1', '2'],
                      'M-DS':   ['1', '2'],
                      'M-RO':   ['1', '2']
                      }
BS1_ENGLISH_GROUPS = ['EN1', 'EN2', 'EN3', 'EN4', 'EN5', 'EN6', 'EN7', 'EN8', 'EN9', 'EN10']
FIRST_COURSE_EN_GROUPS = 10

REMIND_WHEN_LEFT_MINUTES = 10
