import random
import string
import json
import requests
import threading

username_webhook = "Nitro Checker"
avatar_webhook = "your_avatar_webhooks.png"

def clear():
    print("\033c", end="")

def main():
    print("Atom Tools - Discord Nitro Checker")

def ErrorModule(e):
    print(f"ERROR: {e}")

def CheckWebhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code != 200:
            print("Invalid webhook URL or unable to connect.")
            return False
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error checking webhook URL: {e}")
        return False

def ErrorNumber():
    print("Invalid input for threads number.")

def send_webhook(embed_content, webhook_url):
    payload = {
        'embeds': [embed_content],
        'username': username_webhook,
        'avatar_url': avatar_webhook
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

def generate_nitro_code():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return code

def nitro_check(webhook_enabled, webhook_url):
    code_nitro = generate_nitro_code()
    url_nitro = f'https://discord.gift/{code_nitro}'
    
    try:
        response = requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=1)
        if response.status_code == 200:
            if webhook_enabled:
                embed_content = {
                    'title': 'Nitro Valid!',
                    'description': f"**__Nitro:__**\n```{url_nitro}```",
                    'footer': {
                        "text": username_webhook,
                        "icon_url": avatar_webhook,
                    }
                }
                send_webhook(embed_content, webhook_url)
                print(f"GEN_VALID Status: Valid | Nitro: {url_nitro}")
            else:
                print(f"GEN_VALID Status: Valid | Nitro: {url_nitro}")
        else:
            print(f"GEN_INVALID Status: Invalid | Nitro: {url_nitro}")
    except requests.exceptions.RequestException as e:
        print(f"GEN_ERROR Status: Error - {e}")

def request(threads_number, webhook_enabled, webhook_url):
    threads = []
    try:
        for _ in range(threads_number):
            t = threading.Thread(target=nitro_check, args=(webhook_enabled, webhook_url))
            t.start()
            threads.append(t)
    except ValueError:
        ErrorNumber()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        clear()

        webhook_enabled = False
        webhook_input = input("Enable webhook notifications? (y/n): ").strip().lower()
        if webhook_input in ['y', 'yes']:
            webhook_enabled = True
            webhook_url = input("Enter webhook URL: ").strip()
            if not CheckWebhook(webhook_url):
                exit()

        threads_number = int(input("Threads Number: "))

        while True:
            request(threads_number, webhook_enabled, webhook_url)

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        ErrorModule(e)
