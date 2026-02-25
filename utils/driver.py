import undetected_chromedriver as uc
import winreg

def get_chrome_version():
    default_veraion=144
    try:
        key_path = r"SOFTWARE\WOW6432Node\Google\Update\Clients\{8A69D345-D564-463c-AFF1-A69D9E530F96}"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        
        version, _ = winreg.QueryValueEx(key, "pv")
        winreg.CloseKey(key)
        
        return int(version.split('.')[0])
    
    except WindowsError:
        return default_veraion

def get_driver(headless=False):
    version = get_chrome_version()
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        driver = uc.Chrome(
            version_main=version,
            options=options,
            headless=headless,
            use_subprocess=False)
        
        driver.maximize_window()

        return driver
    except Exception as e:
        print(f"GET_DRIVER ERROR: {e}")
        raise e

