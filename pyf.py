
import os,sys,re,time
import datetime as dt

for i in [
'./.vscode/settings.json', \
'./.vscode/tasks.json', \
'./.vscode/extensions.json', \
'./bin/.gitignore', \
'./doc/.gitignore', \
'./lib/.gitignore', \
'./src/.gitignore', \
'./tmp/.gitignore', \
'./gitignore', \
'./pyf.py', \
'./README.md', \
'./Makefile', \
'./apt.txt', \
'./apt.dev', \
'./requirements.txt', \
]: os.system(f'touch {i}')
