from pymino.ext import exceptions
from pymino import Client
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("""
█▀ █▀▀ ▀█▀   █░█ █▀ █▀▀ █▀█ █▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
▄█ ██▄ ░█░   █▄█ ▄█ ██▄ █▀▄ ▄█
""")

DEVICE_ID = None # Если требуется device_id.

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

def main():
    start=0
    while True:
        try:
            client = Client(signature_key="DFA5ED192DDA6E88A12FE12130DC6206B1251E44", device_key="E7309ECC0953C6FA60005B2765F99DBBC965C8E9")
            client.login(email = input("E-mail: "), password = input("Password: "), device_id=DEVICE_ID, use_cache=False)
            gd_print(f"Вошли в аккаунт {client.profile.username}")
            break
        except exceptions.VerificationRequired as e:
            bd_print(f"Необходимо пройти верификацию: {e}")
        except exceptions.InvalidAccountOrPassword:
            bd_print("Неверный логин или пароль. Попробуйте еще раз.")
        except exceptions.InvalidEmail:
            bd_print("Неверный формат e-mail. Попробуйте еще раз.")
        except exceptions.InvalidPassword:
            bd_print("Неверный пароль. Попробуйте еще раз.")
        except exceptions.AccountLoginRatelimited or exceptions.AccountLimitReached:
            bd_print("Превышен лимит запросов. Попробуйте позже.")
        except Exception as e:
            bd_print(e)

    while True:
        try:
            community = input("Ссылка на сообщество: ")
            comId = client.fetch_community_id(community)
            gd_print(f"Получили информацию о сообществе '{client.fetch_community(comId).name}'")
            break
        except exceptions.DataNoLongerExists or exceptions.UnexistentData or exceptions.NoLongerExists:
            bd_print("Сообщество не найдено. Попробуйте еще раз.")
        except exceptions.CommunityDeleted or exceptions.CommunityDisabled:
            bd_print("Сообщество удалено или заблокировано. Попробуйте еще раз.")
        except exceptions.CommunityNoLongerExists:
            bd_print("Сообщество больше не существует (не найдено). Попробуйте еще раз.")
        except Exception as e:
            bd_print(e)

    while True:
        try:
            all_users_uids = set()
            users = client.community.fetch_users(start = start*100, size=100, comId=comId)
            print(f"> Получили пользователей. Проверяем данные...\n")
            for userId, role, is_banned in zip(users.userId, users.role, users.is_user_banned):
                if is_banned != True: # Можно добавить другие условия для фильтрации пользователей. Например: if not role (то есть если пользователь не является администратором)
                    all_users_uids.add(userId)

            if all_users_uids:
                try:
                    with open("users.txt", "a") as file_users:
                        for userId in all_users_uids:
                            file_users.write(f"{userId}\n")
                except Exception as e:
                    bd_print(e)

                start += 1
                gd_print(f"Записали {len(all_users_uids)} пользователей в файл")

            else:
                break
        
        except exceptions.UserNotMemberOfCommunity:
            print("Чтобы получить пользователей сообщества, нужно быть его участником. Вступить в сообщество? (y/n)")
            if input().lower() == "y":
                try:
                    client.join_community(comId)
                    gd_print("Вступили в сообщество")
                except Exception as e:
                    bd_print(e)
            else:
                print("\n> Выход из программы")
                break
        except Exception as e:
            bd_print(e)


if __name__ == '__main__':
    main()
    print("---")
    print()
    gd_print(f"Скрипт завершил свою работу!")
