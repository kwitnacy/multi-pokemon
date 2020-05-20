import time


file_obj = open('log', 'a')

# time.strftime('%h %d %H:%M:%S')

file_obj.write(time.strftime('[%h %d %H:%M:%S') + '] hej\n')
