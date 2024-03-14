ACHTUNG:
Damit die git hooks funktionieren müssen die beiden Dateien hier ins Verzeichnis .git/hooks kopiert werden.

Außerdem muss ein Verzeichnis .git_sensible_backup angelegt werden

Hier die Kommandos

cd ~/CaravanPi
cp .git_hooks/*commit .git/hooks
chmod +x .git/hooks/*commit
mkdir ~/CaravanPi/.git_sensible_backup