import uuid



def get_save_coords():
    # Get the MAC address
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
    print(f"MAC Address: {mac_address}")


    SAVE_BTN_COORDS = (2013, 354,)
    if mac_address == "17:29:bf:99:23:6a":
        # Personal
        SAVE_BTN_COORDS = (2013, 354,)
    elif mac_address in ["7f:7e:5c:29:53:31", "97:24:3f:c7:ac:2f"]:
        # AMD Linux Laptop RED
        SAVE_BTN_COORDS = (1867, 300,)
    return SAVE_BTN_COORDS



def get_coords():
    return {
        "click_desktop_device": (2305, 483,),
        "click_analyze_page_load": (2414, 259,),
        "click_download_menu": (2527, 182,),
        "click_download": (2465, 351,),
        "click_save": (2006, 351,),
        "click_new_report": (2278, 147,),
    }