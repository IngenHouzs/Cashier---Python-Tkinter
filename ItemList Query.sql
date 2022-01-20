DROP TABLE IF EXISTS `item list`;
CREATE TABLE `item list` (
	`ItemName` varchar(255),
    `ItemCode` int(11) NOT NULL AUTO_INCREMENT,
    `ItemPrice` int(11),
    PRIMARY KEY (`ItemCode`)
); 

INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Book of Heroes', 500);   
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Book of Building', 925); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Book of Spells', 925); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Book of Fighting', 925); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Book of Everything', 1200); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Rune of Gold', 2000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Rune of Elixir', 2000);  
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Rune of Dark Elixir', 3000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Rune of Gems', 80000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Hammer of Heroes', 10000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Hammer of Building', 8000);
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Hammer of Spells', 8000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Hammer of Fighting', 8000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Hammer of Everything', 12000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Autumn Queen Skin', 4000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Icy Queen Skin', 4000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Gladiator Queen Skin', 4000);
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Skeleton King Skin', 4000);
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('P.E.K.K.A King Skin', 4000); 
INSERT INTO `item list` (`ItemName`, `ItemPrice`) VALUES ('Jolly King Skin', 4000);                  

SELECT * FROM `item list`;