import os
print os.path.join(os.path.dirname(__file__), 'logs/test.csv')
print __file__ + 'logs/' + 'test' + '.csv'
