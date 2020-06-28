import DBclases
import DBhelper

class Query:
    db=DBhelper.DBHelperclass()
    def __init__(self):
       self.db.change_db("pokemon")
       pass
    def insert_ID (self,instance):
        switch={
            'User':self.db.execute_otherdb("INSERT INTO  `Users` (User_ID, User_name, User_pass) VALUES ("+str(instance.User_ID)+ ", \""+instance.User_name+"\", \""+instance.User_pass+"\")","pokemon"),
            'Pokemon':self.db.execute_otherdb("INSERT INTO  `Pokemons` (`Pokemon_ID`,`Pokemon_name`,`Pokemon_lv`,`Pokemon_exp_to_level`,`Pokemon_move1_ID`,`Pokemon_move2_ID`,`Pokemon_move3_ID`,`Pokemon_move4_ID`,`Poke_ID`,`Char_ID`) VALUES ("+str(instance.Pokemon_ID)+ ", \""+instance.Pokemon_name+"\", "+str(instance.Pokemon_lv)+","+str(instance.Pokemon_exp_to_level)+","+ str(instance.Pokemon_move1_ID)+","+ str(instance.Pokemon_move2_ID)+","+ str(instance.Pokemon_move3_ID)+","+ str(instance.Pokemon_move4_ID)+","+ str(instance.Poke_ID)+","+ str(instance.Char_ID)+")","pokemon"),
            'World':self.db.execute_otherdb("INSERT INTO  `Worlds` (World_ID, World_name ) VALUES ("+str(instance.World_ID)+ ", \""+instance.World_name+"\""+")","pokemon"),
            'Character':self.db.execute_otherdb("INSERT INTO  `Characters` (Char_ID,User_ID, World_ID, Char_name) VALUES ("+str(instance.Char_ID)+ ", "+str(instance.User_ID)+", "+str(instance.World_ID)+",\""+instance.Char_name+"\")","pokemon"),
            }
        switch.get(instance.__class__.__name__)
    
    def insert_no_ID (self,instance):
        switch={
            'User':self.db.execute_otherdb("INSERT INTO  `Users` (User_name, User_pass) VALUES ("+ " \""+instance.User_name+"\", \""+instance.User_pass+"\")","pokemon"),
            'Pokemon':self.db.execute_otherdb("INSERT INTO  `Pokemons` (`Pokemon_name`,`Pokemon_lv`,`Pokemon_exp_to_level`,`Pokemon_move1_ID`,`Pokemon_move2_ID`,`Pokemon_move3_ID`,`Pokemon_move4_ID`,`Poke_ID`,`Char_ID`) VALUES ("+"\""+instance.Pokemon_name+"\", "+str(instance.Pokemon_lv)+","+str(instance.Pokemon_exp_to_level)+","+ str(instance.Pokemon_move1_ID)+","+ str(instance.Pokemon_move2_ID)+","+ str(instance.Pokemon_move3_ID)+","+ str(instance.Pokemon_move4_ID)+","+ str(instance.Poke_ID)+","+ str(instance.Char_ID)+")","pokemon"),
            'World':self.db.execute_otherdb("INSERT INTO  `Worlds` (World_ID, World_name ) VALUES ("+ " \""+instance.World_name+"\""+")","pokemon"),
            'Character':self.db.execute_otherdb("INSERT INTO  `Characters` (User_ID, World_ID, Char_name) VALUES ("+" "+str(instance.User_ID)+", "+str(instance.World_ID)+",\""+instance.Char_name+"\")","pokemon"),
            }
        switch.get(instance.__class__.__name__)

    def update_int(self,ID,update_value,column,table_type):
        switch={
            'User':db.execute_otherdb("UPDATE Users Set "+ column +"="+str(update_value)+" where User_ID="+str(ID),"pokemon"),
            'Users':db.execute_otherdb("UPDATE Users Set "+ column +"="+str(update_value)+" where User_ID="+str(ID),"pokemon"),
            'Pokemon':db.execute_otherdb("UPDATE Pokemons Set "+ column +"="+str(update_value)+" where Pokemon_ID="+str(ID),"pokemon"),
            'Pokemons':db.execute_otherdb("UPDATE Users Set "+ column +"="+str(update_value)+" where Pokemon_ID="+str(ID),"pokemon"),
            'World':db.execute_otherdb("UPDATE Users Set "+ column +"="+str(update_value)+" where World_ID="+str(ID),"pokemon"),
            'Worlds':db.execute_otherdb("UPDATE Users Set "+ column +"="+str(update_value)+" where World_ID="+str(ID),"pokemon"),
            'Character':db.execute_otherdb("UPDATE Pokemons Set "+ column +"="+str(update_value)+" where Pokemon_ID="+str(ID),"pokemon"),
            'Characters':db.execute_otherdb("UPDATE Characters Set "+ column +"="+str(update_value)+" where Char_ID="+str(ID),"pokemon"),
            }
        switch.get(table_type)
        

    def update_string(self,ID,update_value,column,table_type):
        switch={
            'User':db.execute_otherdb("UPDATE Users Set "+ column +"=\""+str(update_value)+"\" where User_ID="+str(ID),"pokemon"),
            'Users':db.execute_otherdb("UPDATE Users Set "+ column +"=\""+str(update_value)+"\" where User_ID="+str(ID),"pokemon"),
            'Pokemon':db.execute_otherdb("UPDATE Pokemons Set "+ column +"=\""+str(update_value)+"\" where Pokemon_ID="+str(ID),"pokemon"),
            'Pokemons':db.execute_otherdb("UPDATE Users Set "+ column +"=\""+str(update_value)+"\" where Pokemon_ID="+str(ID),"pokemon"),
            'World':db.execute_otherdb("UPDATE Users Set "+ column +"=\""+str(update_value)+"\" where World_ID="+str(ID),"pokemon"),
            'Worlds':db.execute_otherdb("UPDATE Users Set "+ column +"=\""+str(update_value)+"\" where World_ID="+str(ID),"pokemon"),
            'Character':db.execute_otherdb("UPDATE Pokemons Set "+ column +"=\""+str(update_value)+"\" where Pokemon_ID="+str(ID),"pokemon"),
            'Characters':db.execute_otherdb("UPDATE Characters Set "+ column +"=\""+str(update_value)+"\" where Char_ID="+str(ID),"pokemon"),
            }
        switch.get(table_type)
    def update(self,ID,update_value,column,table_type):
        if(isinstance(update_value,int)):
             update_int(self,ID,update_value,column,table_type)
        else:
             update_string(self,ID,update_value,column,table_type)
    def delete(table_type,ID):
        switch={
            'User':db.execute_otherdb("DELETE FROM Users where User_ID="+str(ID),"pokemon"),
            'Users':db.execute_otherdb("DELETE FROM Users where User_ID="+str(ID),"pokemon"),
            'Pokemon':db.execute_otherdb("DELETE FROM Pokemons where Pokemon_ID="+str(ID),"pokemon"),
            'Pokemons':db.execute_otherdb("DELETE FROM Users where Pokemon_ID="+str(ID),"pokemon"),
            'World':db.execute_otherdb("DELETE FROM Users where World_ID="+str(ID),"pokemon"),
            'Worlds':db.execute_otherdb("DELETE FROM Users where World_ID="+str(ID),"pokemon"),
            'Character':db.execute_otherdb("DELETE FROM Pokemons where Pokemon_ID="+str(ID),"pokemon"),
            'Characters':db.execute_otherdb("DELETE FROM Characters  where Char_ID="+str(ID),"pokemon"),
            }
        switch.get(table_type)

        