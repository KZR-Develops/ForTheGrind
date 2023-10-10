import datetime

boot_time = None

def set_boot_time():
    global boot_time
    boot_time = datetime.datetime.now()

def get_boot_time():
    return boot_time

def format_boot_time(format="%Y-%m-%d %H:%M:%S"):
    boot_time = get_boot_time()
    if boot_time is None:
        return "Boot time is not set. Make sure to set the boot time using set_boot_time() in your main script."

    formatted_boot_time = boot_time.strftime(format)
    return formatted_boot_time