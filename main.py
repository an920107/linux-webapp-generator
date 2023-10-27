import os
from threading import Thread


HOME = os.environ.get("HOME")
USER = os.environ.get("USER")

EDGE_EXEC_PATH = "/opt/microsoft/msedge/microsoft-edge"
CHROME_EXEC_PATH = "/opt/google/chrome/google-chrome"


class Configuration:
    browser: int
    app_name: str
    app_url: str
    icon_path: str

    @property
    def exec_path(self):
        if self.browser == 1:
            return CHROME_EXEC_PATH
        else:
            return EDGE_EXEC_PATH


def build_job(config: Configuration) -> None:
    config_path = f"{HOME}/.config/webapp-{config.app_name.lower()}"
    os.system(f"mkdir -p {config_path}")
    os.system(f"cp {config.icon_path} {config_path}/icon.png")
    with open(f"{HOME}/.local/share/applications/{config.app_name.lower()}.desktop", "w") as desktop_conf:
        desktop_conf.write("[Desktop Entry]\n")
        desktop_conf.write("Version=1.0\n")
        desktop_conf.write("Terminal=false\n")
        desktop_conf.write("Type=Application\n")
        desktop_conf.write(f"Name={config.app_name}\n")
        desktop_conf.write(
            f"Exec={config.exec_path} --user-data-dir={config_path} --class={config.app_name.lower()} --app='{config.app_url}' --window-size=1280,720 --window-position=320,180\n")
        desktop_conf.write(f"Icon={config_path}/icon.png\n")
        desktop_conf.write(f"StartupWMClass={config.app_name.lower()}\n")


def print_divider() -> None:
    print("=" * 40)


def main() -> None:
    config = Configuration()

    print("Welcome to Linux Webapp Generator!")
    print_divider()

    print("Which browser do you want to use?")
    print("0. Microsoft Edge")
    print("1. Google Chrome")
    config.browser = int(input())
    print_divider()

    print("Please enter the name of the webapp (eg: ChatGPT)")
    config.app_name = input()
    print_divider()

    print("Please enter the URL of the webapp (eg: https://example.com/)")
    config.app_url = input()
    print_divider()

    print("Please enter the the absolute path of the icon (eg: /home/user/icon.png)")
    config.icon_path = input()
    print_divider()

    print("Building...")
    build_thread = Thread(target=build_job, args=[config])
    try:
        build_thread.start()
        build_thread.join()
        print("Success!")
    except:
        pass


if __name__ == "__main__":
    main()
