from aminofix import *
import threading
import aminofix
import time
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("""
█▀ █▀▀ ▀█▀   █░█ █▀ █▀▀ █▀█ █▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
▄█ ██▄ ░█░   █▄█ ▄█ ██▄ █▀▄ ▄█
""")

def gd_print(value):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    result = f"\n>{green_color} {value} {reset_color}\n"
    print(result)

def bd_print(value):
    red_color = '\033[31m'
    reset_color = '\033[0m'
    result = f"\n>{red_color} {value} {reset_color}\n"
    print(result)

def get_users(start, sub_clientz, all_people_set):
    try:
        all_people = sub_clientz.get_all_users(type="recent", start=start, size=100)
        for userId in all_people.profile.userId:
            all_people_set.add(userId)
        if all_people_set:
            try:
                blocked_users = set(sub_clientz.get_blocker_users(start=0, size=100))
                all_people_set -= blocked_users
            except:
                pass
    except exceptions.IpTemporaryBan:
        bd_print("Ошибка: вас забанили по ip. Скрипт продолжит работу через 360 секунд")
        time.sleep(360)
    except exceptions.AccountLimitReached or exceptions.TooManyRequests:
        bd_print("Ошибка: Слишком много запросов. Скрипт остановлен")
        exit()
    except exceptions.InvalidRequest:
        bd_print("Ошибка: инвалидный запрос")
    except exceptions.UserHasBeenDeleted:
        pass
    except exceptions.UserUnavailable:
        pass
    except Exception as error:
        bd_print(f"Ошибка: {error}")

def main():
    while True:
        try:
            clientz = aminofix.Client()
            clientz.login(email = input("E-mail: "), password = input("пароль: "))
            gd_print(f"Вошли в аккаунт '{clientz.profile.nickname}'")
            break
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    while True:
        try:
            community_link = clientz.get_from_code(input("Ссылка на сообщество: "))
            comId = community_link.comId
            sub_clientz = aminofix.SubClient(comId = comId, profile = clientz.profile)
            gd_print(f"Получили информацию о сообществе '{community_link.community.name.strip()}'")
            break
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    if not os.path.exists("nonusers.txt"):
        with open("nonusers.txt", "w") as file:
            pass

    all_people_set = set()
    threads = []
    for i in range(0, 10000, 100):
        t = threading.Thread(target=get_users, args=(i, sub_clientz, all_people_set))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    gd_print(f"Записали {len(all_people_set)} пользователей в список")
    with open("nonusers.txt", "a") as file:
        for elem in all_people_set:
            file.write(elem + "\n")

if __name__ == '__main__':
    main()
    print("---")
    print()
    gd_print(f"Скрипт завершил свою работу!")