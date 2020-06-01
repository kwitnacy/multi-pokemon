
import pymysql
import DBclases
import queries
import DBhelper

    

         
create_table_Users="CREATE TABLE IF NOT EXISTS `Users` (`User_ID` int(12) NOT NULL auto_increment,`User_name` varchar(20) NOT NULL,`User_pass` varchar(255)  NOT NULL, PRIMARY KEY (`User_id`));" 
create_table_Characters="CREATE TABLE IF NOT EXISTS `Characters` (`Char_ID` int(12) NOT NULL auto_increment,`User_ID` int(12) NOT NULL,`World_ID` int(12)  NOT NULL,`Char_name` varchar(20) NOT NULL,PRIMARY KEY (`Char_ID`),CONSTRAINT FK_UsersCharacters FOREIGN KEY (`User_ID`) References Users(User_ID), CONSTRAINT FK_WorldsCharacters FOREIGN KEY (`World_ID`) References Worlds(World_ID) );"
create_table_Worlds="CREATE TABLE IF NOT EXISTS `Worlds` (`World_ID` int(12) NOT NULL auto_increment,`World_name` varchar(20) NOT NULL, PRIMARY KEY (`World_ID`));" 
create_table_Pokemons="CREATE TABLE IF NOT EXISTS `Pokemons` (`Pokemon_ID` int(12) NOT NULL auto_increment,`Pokemon_name` varchar(20) NOT NULL,`Pokemon_lv` int(12)  NOT NULL,`Pokemon_exp_to_level` int(20) NOT NULL,`Pokemon_move1_ID` int(20) NOT NULL,`Pokemon_move2_ID` int(20) NOT NULL,`Pokemon_move3_ID` int(20) NOT NULL,`Pokemon_move4_ID` int(20) NOT NULL,`Poke_ID` int(12)  NOT NULL,`Char_ID` int(12) NOT NULL ,PRIMARY KEY (`Pokemon_ID`),CONSTRAINT FK_PokemonsCharacters FOREIGN KEY (Char_ID) References Characters(Char_ID) );"
helper=DBhelper.DBHelper()
#helper.execute("DROP pokemon")
#helper.execute("CREATE DATABASE pokemon")
helper.change_db("pokemon")
helper.execute(create_table_Users)
helper.execute(create_table_Worlds)
helper.execute(create_table_Characters)

helper.execute(create_table_Pokemons)
#helper.execute("INSERT INTO `Users`(User_ID, User_name, User_pass) VALUES (1,\"dd\",\"niech\")")
a=DBclases.User(3,"d","32")
query=queries.Query()
query.insert(a)
 