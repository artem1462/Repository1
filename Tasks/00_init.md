# Задача 00 — Установка Git и подключение к репозиторию

Подготовительный шаг.

## Часть 1 — Установка Git

### Шаг 1 — Открыть PowerShell

Нажмите `Win + X` → выберите **Windows PowerShell** или **Терминал**.  
Либо `Win + R` и ввести powershell

Убедитесь что Git ещё не установлен:

```powershell
git --version
```

Если видите `git version 2.x.x` — Git уже есть, переходите к Части 2.

### Шаг 2 — Установить через winget

`winget` — стандартный менеджер пакетов Windows, доступен начиная с Windows 10 (1709):

```powershell
winget install --id Git.Git -e --source winget
```

Флаг `-e` означает точное совпадение по ID — чтобы не поставить что-то лишнее.  
Установка занимает 1–2 минуты.

### Шаг 3 — Перезапустить PowerShell и проверить

Закройте PowerShell и откройте заново, затем:

```powershell
git --version
```

Должны увидеть что-то вроде: `git version 2.45.2.windows.1`

---

## Часть 2 — Первичная настройка Git

Git должен знать ваше имя и email — они будут указаны в каждом коммите.  
Используйте те же данные, что и при регистрации на GitHub.

```powershell
git config --global user.name "Имя Фамилия"
git config --global user.email "ваш@email.com"
```

Настроить редактор по умолчанию (рекомендуется VS Code если установлен):

```powershell
git config --global core.editor "code --wait"
```

Проверить что всё сохранилось:

```powershell
git config --list
```

---

## Часть 3 — Подключение к GitHub

### Шаг 1 — Сгенерировать SSH-ключ

SSH-ключ позволяет подключаться к GitHub без ввода пароля при каждом `push`.

```powershell
ssh-keygen -t ed25519 -C "ваш@email.com"
```

На все вопросы можно нажимать Enter (путь по умолчанию, без пароля на ключ).  
В итоге создадутся два файла:
'C:\Users<вы>.ssh\id_ed25519'      ← приватный ключ (никому не показывать)
'C:\Users<вы>.ssh\id_ed25519.pub'  ← публичный ключ (этот отдаём GitHub)

### Шаг 2 — Скопировать публичный ключ

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | clip
```

Ключ теперь в буфере обмена.

### Шаг 3 — Добавить ключ на GitHub

1. Откройте [github.com](https://github.com) → войдите в аккаунт
2. Нажмите на аватар → **Settings**
3. В левом меню: **SSH and GPG keys**
4. Нажмите **New SSH key**
5. Title: например `university-laptop`
6. Key: вставьте из буфера (`Ctrl+V`)
7. Нажмите **Add SSH key**

### Шаг 4 — Проверить подключение

```powershell
ssh -T git@github.com
```

Ожидаемый ответ:
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.

Если появилось `successfully authenticated` — всё готово.

---

## Часть 4 — Клонировать репозиторий

### Шаг 1 — Получить SSH-ссылку

На странице репозитория на GitHub:  
нажмите **Code** → вкладка **SSH** → скопируйте ссылку вида `git@github.com:username/repo.git`

> Используйте именно SSH-ссылку, а не HTTPS — иначе GitHub будет спрашивать пароль при каждом push.

### Шаг 2 — Выбрать папку и клонировать

```powershell
cd C:\Users\<вы>\Documents       # или любая удобная папка
git clone git@github.com:<username>/<repo>.git
cd <repo>
```

### Шаг 3 — Убедиться что всё работает

```powershell
git status
git log --oneline
python <ваш_файл>.py
```

`git status` должен вывести:

Если все работает то можно пробовать делать клон репозитория (задача 01)
