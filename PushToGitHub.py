from os import listdir
from subprocess import call
commitMessage = raw_input('->')

files = [f for f in listdir('./') if f.endswith('py') or f.endswith('txt')]
add = ['git', 'add'] + files
call(add)
call(['git', 'commit', '-m', commitMessage])
call(['git', 'push', 'origin', 'master'])