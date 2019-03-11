drop table SongRank;
drop table SongArtist;
drop table Song;
drop table Album;
drop table Artist;

CREATE TABLE `Artist` (
  `artistNo` int(10) unsigned NOT NULL,
  `artistName` varchar(128) DEFAULT NULL,
  `artistType` varchar(128) DEFAULT NULL,
  `emc` varchar(128) DEFAULT NULL,
  `debutDate` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`artistNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Album` (
  `albumNo` int(10) unsigned NOT NULL,
  `albumTitle` varchar(256) NOT NULL,
  `agency` varchar(128) DEFAULT NULL,
  `releaser` varchar(128) DEFAULT NULL,
  `releaseDate` varchar(128) DEFAULT NULL,
  `albumGenre` varchar(128) DEFAULT NULL,
  `rating` tinyint(3) unsigned DEFAULT NULL,
  `artistNo` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`albumNo`),
  KEY `fk_Album_Artist_idx` (`artistNo`),
  CONSTRAINT `fk_Album_Artist` FOREIGN KEY (`artistNo`) REFERENCES `Artist` (`artistNo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Song` (
  `songNo` int(10) unsigned NOT NULL,
  `songTitle` varchar(256) NOT NULL,
  `genre` varchar(128) DEFAULT NULL,
  `albumNo` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`songNo`),
  KEY `fk_Song_Album_idx` (`albumNo`),
  CONSTRAINT `fk_Song_Album` FOREIGN KEY (`albumNo`) REFERENCES `Album` (`albumNo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `SongArtist` (
  `songArtistID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `songNo` int(10) unsigned NOT NULL,
  `artistNo` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`songArtistID`),
  KEY `fk_SA_Song_idx` (`songNo`),
  KEY `fk_SA_Artist_idx` (`artistNo`),
  CONSTRAINT `fk_SA_Artist` FOREIGN KEY (`artistNo`) REFERENCES `Artist` (`artistNo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_SA_Song` FOREIGN KEY (`songNo`) REFERENCES `Song` (`songNo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `SongRank` (
  `rankID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `songNo` int(10) unsigned NOT NULL,
  `rankDate` varchar(128) NOT NULL,
  `likeCnt` int(10) unsigned DEFAULT NULL,
  `rank` smallint(5) unsigned DEFAULT NULL,
  `crawlDate` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`rankID`),
  UNIQUE KEY `sNrD` (`songNo`,`rankDate`),
  CONSTRAINT `fk_SR_Song` FOREIGN KEY (`songNo`) REFERENCES `Song` (`songNo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

