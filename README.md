# jenkins_backup

Скрипт для автоматического резервного копирования job'ов из Jenkins.

Обходит job'ы типа Folder с главной страницы Jenkins и сохраняет `config.xml` каждого вложенного job'а на диск.

## Конфигурация

Вся конфигурация передаётся через переменные окружения:

- `JENKINS_SERVER="jenkins.jtprog.ru"` — хост Jenkins;
- `JENKINS_USER="username"` — пользователь, под которым подключаться в Jenkins;
- `JENKINS_API_KEY="xxxxx"` — API key для пользователя `username`;
- `JENKINS_JOBS_DIR` — директория для XML-файлов (необязательно, по умолчанию `jenkins_jobs/`).

## Запуск локально

Проект управляется через [uv](https://docs.astral.sh/uv/), требуется Python 3.14 (uv поставит его сам):

```bash
JENKINS_SERVER="jenkins.jtprog.ru" JENKINS_API_KEY="xxxxx" JENKINS_USER="username" uv run jenkins-backup.py
```

## Запуск в Docker

```bash
docker build -t jtprogru/backup-jenkins-jobs .
docker run --rm \
  -e JENKINS_SERVER="jenkins.jtprog.ru" \
  -e JENKINS_USER="username" \
  -e JENKINS_API_KEY="xxxxx" \
  -v "$(pwd)/jenkins_jobs:/backup" \
  jtprogru/backup-jenkins-jobs
```

Или через docker compose (переменные берутся из окружения либо из `.env`):

```bash
docker compose run --rm jenkins-backup
```

## Запуск как CronJob в Kubernetes

Образ рассчитан на one-shot запуск: контейнер выполняет бэкап и завершается. Пример манифеста:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: jenkins-backup
spec:
  schedule: "0 3 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: jenkins-backup
              image: jtprogru/backup-jenkins-jobs:latest
              env:
                - name: JENKINS_SERVER
                  value: jenkins.jtprog.ru
                - name: JENKINS_USER
                  valueFrom:
                    secretKeyRef:
                      name: jenkins-backup
                      key: user
                - name: JENKINS_API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: jenkins-backup
                      key: api-key
              volumeMounts:
                - name: backup
                  mountPath: /backup
          volumes:
            - name: backup
              persistentVolumeClaim:
                claimName: jenkins-backup
```
