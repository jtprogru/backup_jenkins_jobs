# jenkins_backup
Скрипт для автоматического резервного копирования job'ов из Jenkins

Для запуска необходимо передать следующие переменные:
- `JENKINS_SERVER="jenkins.jtprog.ru"` - хост Jenkins;
- `JENKINS_USER="username"` - пользователь под которым подключаться в Jenkins;
- `JENKINS_API_KEY="xxxxx"` - API key для пользователя `username`;

Переменные можно напрямую указать в файле [`config.py`](config.py). Так же в этом файле указывается относительный или абсолютный путь до директории, куда будут складываться XML-файлы.


Пример запуска:
```bash
JENKINS_SERVER="jenkins.jtprog.ru" JENKINS_API_KEY="xxxxx" JENKINS_USER="username" python jenkins-backup.py
```

Написано на Python 3.7

