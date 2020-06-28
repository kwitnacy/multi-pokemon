
import pymysql
import DBclases
import queries
from DBhelper import DBHelperclass

    

         
create_table_Users = "CREATE TABLE IF NOT EXISTS `Users` (`user_ID` int(12) NOT NULL auto_increment,`user_name` varchar(20) NOT NULL,`passwd_hash` varchar(255) NOT NULL,`ip_addr` varchar(21),`loc` varchar(100), PRIMARY KEY (`User_id`));" 
create_table_Characters = "CREATE TABLE IF NOT EXISTS `Characters` (`Char_ID` int(12) NOT NULL auto_increment,`User_ID` int(12) NOT NULL,`World_ID` int(12)  NOT NULL,`Char_name` varchar(20) NOT NULL,PRIMARY KEY (`Char_ID`),CONSTRAINT FK_UsersCharacters FOREIGN KEY (`User_ID`) References Users(User_ID), CONSTRAINT FK_WorldsCharacters FOREIGN KEY (`World_ID`) References Worlds(World_ID) );"
create_table_Worlds = "CREATE TABLE IF NOT EXISTS `Worlds` (`World_ID` int(12) NOT NULL auto_increment,`World_name` varchar(20) NOT NULL, PRIMARY KEY (`World_ID`));" 
create_table_Pokemons = "CREATE TABLE IF NOT EXISTS `Pokemons` (`Pokemon_ID` int(12) NOT NULL auto_increment,`Pokemon_name` varchar(20) NOT NULL,`Pokemon_lv` int(12)  NOT NULL,`Pokemon_exp_to_level` int(20) NOT NULL,`Pokemon_move1_ID` int(20) NOT NULL,`Pokemon_move2_ID` int(20) NOT NULL,`Pokemon_move3_ID` int(20) NOT NULL,`Pokemon_move4_ID` int(20) NOT NULL,`Poke_ID` int(12)  NOT NULL,`Char_ID` int(12) NOT NULL ,PRIMARY KEY (`Pokemon_ID`),CONSTRAINT FK_PokemonsCharacters FOREIGN KEY (Char_ID) References Characters(Char_ID) );"

helper = DBHelperclass()
helper.execute("DROP DATABASE IF EXISTS pokemon")
helper.execute("CREATE DATABASE IF NOT EXISTS pokemon")

helper.change_db("pokemon")
helper.execute(create_table_Users)
helper.execute(create_table_Worlds)
helper.execute(create_table_Characters)
helper.execute(create_table_Pokemons)

helper.execute("INSERT INTO `Users`(user_ID, user_name, passwd_hash) VALUES (1,\"kwitnoncy\",\"dzien_dobry\")")

temp_users = helper.fetch("SELECT * FROM Users")

d = { x['user_name'] : x for x in temp_users}
d['test'] = {
	'user_name': 'test',
	'passwd_hash': 'testastest',
	'ip_addr': None,
	'loc': None,
	'user_ID': 0,
}

for row in d.values():
	if row['user_ID'] != 0:
		print('nie dodano', row)
	else:
		print(row)
		q = queries.Query()
		print(*row.values())
		
		q.insert_no_ID(DBclases.User(row['user_ID'], row['user_name'], row['passwd_hash'], None, None))
		print('dodano:', row)
