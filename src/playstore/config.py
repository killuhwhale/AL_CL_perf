import uuid
import os



def get_save_coords():
    # Get the MAC address
    user = os.getenv("USER")
    print(f"User: {user}")


    SAVE_BTN_COORDS = (2013, 354,)
    if user == "killuh":
        # Personal
        SAVE_BTN_COORDS = (1853, 356,)
    elif user == "appval002":
        # AMD Linux Laptop RED
        SAVE_BTN_COORDS = (1867, 300,)
    return SAVE_BTN_COORDS



def get_coords():
    return {
        "click_desktop_device": (2305, 476,),

        "click_metric_a11y": (2306, 568,),
        "click_metric_bpractices": (2306, 593,),
        "click_metric_seo": (2306, 616,),

        "click_analyze_page_load": (2414, 259,),
        "click_download_menu": (2527, 182,),
        "click_download": (2465, 351,),
        "click_new_report": (2278, 147,),
        "click_save": get_save_coords()
    }