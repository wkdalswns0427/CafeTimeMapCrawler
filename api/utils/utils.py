from datetime import datetime

class utils:
    def __init__(self) -> None:
        pass

    def get_time(self)->str:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time
    
    def compare_time(self, cur_time : str, close_time : str) -> bool:
        cur_time_l = cur_time.split(":")
        close_time_l = close_time.split(":")
        try:
            if int(cur_time_l[0]) < int(close_time_l[0]):
                return True
            elif int(cur_time_l[0]) == int(close_time_l[0]):
                if int(cur_time_l[1]) < int(close_time_l[1]):
                    return True
                else:
                    return False
            else :
                return False
        except:
            return False