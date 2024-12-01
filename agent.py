

class Movement:
    @staticmethod
    def move_up(hor, ver) -> tuple:
        return hor, ver - 1
    
    @staticmethod
    def move_down(hor, ver) -> tuple:
        return hor, ver + 1
    
    @staticmethod
    def move_left(hor, ver) -> tuple:
        return hor - 1, ver
    
    @staticmethod
    def move_right(hor, ver) -> tuple:
        return hor + 1, ver