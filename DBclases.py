
class User:
    User_ID=0
    User_name=""
    User_pass=""
    def __init__(self, 
                 User_ID,
                 User_name,
                 User_pass ):
        self.User_ID=User_ID
        self.User_name=User_name
        self.User_pass=User_pass


class Pokemon:
    Pokemon_ID=""
    Pokemon_name=""
    Pokemon_LV=""
    Pokemon_exp_to_level=""
    Pokemon_move1_ID=""
    Pokemon_move2_ID=""
    Pokemon_move3_ID=""
    Pokemon_move4_ID=""
    Poke_ID=""
    Char_ID=""
    def __init__(self, 
                Pokemon_ID,
                Pokemon_name,
                Pokemon_LV,
                Pokemon_exp_to_level,
                Pokemon_move1_ID,
                Pokemon_move2_ID,
                Pokemon_move3_ID,
                Pokemon_move4_ID,
                Poke_ID,
                Char_ID):
        self.Char_ID=Char_ID
        self.Pokemon_ID=Pokemon_ID
        self.Pokemon_name=Pokemon_name
        self.Pokemon_LV=Pokemon_LV
        self.Pokemon_exp_to_level=Pokemon_exp_to_level
        self.Pokemon_move1_ID=Pokemon_move1_ID
        self.Pokemon_move2_ID=Pokemon_move2_ID
        self.Pokemon_move3_ID=Pokemon_move3_ID
        self.Pokemon_move4_ID=Pokemon_move4_ID
        self.Poke_ID=Poke_ID
        self.CharID=Char_ID

class World:
    World_ID=""
    World_name=""
    def __init__(self,World_ID,World_name):
        self.World_ID=World_ID
        self.World_name=World_name
    

class Character:
    Char_ID=""
    User_ID=""
    World_ID=""
    Char_name=""
    def __init__(self,Char_ID,User_ID,World_ID,Char_name):
        self.Char_ID=Char_ID
        self.User_ID=User_ID
        self.World_ID=World_ID
        self.Char_name=Char_name
    
    
    
    
    

