import process_BAT_ALL_MAKE_HTML
import process_BAT_SINGLE_VEH_HTML


def clean_bat_runner():


    process_BAT_SINGLE_VEH_HTML.BAT_cleaned_SOLD_Data()
    process_BAT_ALL_MAKE_HTML.BAT_cleaned_SOLD_Data()


if __name__ == '__main__':

    clean_bat_runner()