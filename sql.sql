/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.5.20-log : Database - pocket
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`pocket` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `pocket`;

/*Table structure for table `caste` */

DROP TABLE IF EXISTS `caste`;

CREATE TABLE `caste` (
  `ccid` int(11) NOT NULL AUTO_INCREMENT,
  `cuserid` int(11) DEFAULT NULL,
  `crelegion` varchar(200) DEFAULT NULL,
  `ccaste` varchar(200) DEFAULT NULL,
  `category` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ccid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `caste` */

insert  into `caste`(`ccid`,`cuserid`,`crelegion`,`ccaste`,`category`,`status`) values (1,4,'HINDU','THIYYA','OBC','Approved');

/*Table structure for table `certificate` */

DROP TABLE IF EXISTS `certificate`;

CREATE TABLE `certificate` (
  `certificate_id` int(11) NOT NULL AUTO_INCREMENT,
  `certificate` varchar(100) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `proof` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`certificate_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `certificate` */

insert  into `certificate`(`certificate_id`,`certificate`,`userid`,`proof`) values (1,'/static/certificate//220129-160331.jpg',7,'SSLC');

/*Table structure for table `clerk` */

DROP TABLE IF EXISTS `clerk`;

CREATE TABLE `clerk` (
  `login_id` int(11) NOT NULL,
  `c_name` varchar(200) NOT NULL,
  `c_place` varchar(200) NOT NULL,
  `c_pin` int(200) NOT NULL,
  `c_post` varchar(200) NOT NULL,
  `c_district` varchar(200) NOT NULL,
  `c_image` varchar(200) NOT NULL,
  `c_qualification` varchar(200) NOT NULL,
  `c_email` varchar(200) NOT NULL,
  `cjoining_date` date NOT NULL,
  `cending_date` date NOT NULL,
  `c_phone` int(200) NOT NULL,
  `d_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `clerk` */

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `userid` int(11) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `c_date` date DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `reply_date` date DEFAULT NULL,
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`userid`,`complaint`,`c_date`,`reply`,`reply_date`,`complaint_id`) values (4,'','2022-01-28','pending','0000-00-00',1);

/*Table structure for table `department_add` */

DROP TABLE IF EXISTS `department_add`;

CREATE TABLE `department_add` (
  `dept_id` int(11) NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(200) DEFAULT NULL,
  `certificate_name` varchar(200) DEFAULT NULL,
  `d_details` varchar(200) DEFAULT NULL,
  `proof_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `department_add` */

insert  into `department_add`(`dept_id`,`dept_name`,`certificate_name`,`d_details`,`proof_id`) values (1,'Revenue','Marriage Certificate','Certificate Issuing','SSLC,AADHAR,WEDDING INVITATION'),(2,'Revenue','Income Certificate','Certificate Issuing','RATION CARD,INCOME PROOF,SALARY CERTIFICATE'),(3,'Revenue','Caste Certificate','Certificate Issuing','SSLC,AADHAR,RATION CARD,CASTE PROOF'),(4,'Revenue','Nativity Certificate','Certificate Issuing','SSLC,AADHAR,RATION CARD,BIRTH CERTIFICATE');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `fuser_id` int(11) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`fuser_id`,`feedback`,`date`) values (1,4,'super','2022-01-29');

/*Table structure for table `income` */

DROP TABLE IF EXISTS `income`;

CREATE TABLE `income` (
  `inc_id` int(11) NOT NULL AUTO_INCREMENT,
  `inc_userid` int(11) DEFAULT NULL,
  `income_source` varchar(200) DEFAULT NULL,
  `amount` int(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`inc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `income` */

insert  into `income`(`inc_id`,`inc_userid`,`income_source`,`amount`,`status`) values (1,4,'Business',4,'Approved'),(2,7,'Business',20000000,'Approved');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `usertype` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','admin','admin'),(2,'village123@gmail.com','v','VILLAGE_OFFICER'),(3,'clerk@gmail.com','c','CLERK'),(4,'athul@gmail.com','123','USER'),(5,'anagha@gmail.com','11','USER'),(6,'ahh@gmail.com','1','USER'),(7,'sanjay@gmail.com','san','USER'),(8,'arjun@gmail.com','ar','USER');

/*Table structure for table `marriage` */

DROP TABLE IF EXISTS `marriage`;

CREATE TABLE `marriage` (
  `mcid` int(11) NOT NULL AUTO_INCREMENT,
  `wmcuserid` int(11) DEFAULT NULL,
  `hmcuserid` int(11) DEFAULT NULL,
  `marriage_date` date DEFAULT NULL,
  `mlocation` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`mcid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `marriage` */

insert  into `marriage`(`mcid`,`wmcuserid`,`hmcuserid`,`marriage_date`,`mlocation`,`status`) values (1,5,4,'2022-01-20','Dubai','Approved');

/*Table structure for table `nativity` */

DROP TABLE IF EXISTS `nativity`;

CREATE TABLE `nativity` (
  `ncid` int(11) NOT NULL AUTO_INCREMENT,
  `ncuserid` int(11) DEFAULT NULL,
  `fcase_state` varchar(200) DEFAULT NULL,
  `f_district` varchar(200) DEFAULT NULL,
  `f_taluk` varchar(200) DEFAULT NULL,
  `f_village` varchar(200) DEFAULT NULL,
  `m_district` varchar(200) DEFAULT NULL,
  `m_taluk` varchar(200) DEFAULT NULL,
  `m_village` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ncid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `nativity` */

insert  into `nativity`(`ncid`,`ncuserid`,`fcase_state`,`f_district`,`f_taluk`,`f_village`,`m_district`,`m_taluk`,`m_village`,`status`) values (2,4,'Kerala','kannur','Kannur','Vellad','kannur','Taliparamba','Kannur','Approved');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `n_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`n_id`,`notification`,`date`) values (1,'dedededededededededed','2022-01-28');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(100) DEFAULT NULL,
  `u_name` varchar(200) DEFAULT NULL,
  `gender` varchar(200) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `housename` varchar(200) DEFAULT NULL,
  `place` varchar(200) DEFAULT NULL,
  `post` varchar(200) DEFAULT NULL,
  `pin` int(200) DEFAULT NULL,
  `district` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `phoneno` int(200) DEFAULT NULL,
  `village` varchar(200) DEFAULT NULL,
  `taluk` varchar(200) DEFAULT NULL,
  `name_of_local_body` varchar(200) DEFAULT NULL,
  `father_name` varchar(200) DEFAULT NULL,
  `mother_name` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`u_name`,`gender`,`dob`,`housename`,`place`,`post`,`pin`,`district`,`email`,`phoneno`,`village`,`taluk`,`name_of_local_body`,`father_name`,`mother_name`) values (2,'village officer','male','2022-01-12','vadakeyil','kannur','taliparamba',670571,'kannur','village123@gmail.com',2147483647,'kochi','taliparamba','suresh','suresh','sruthi'),(3,'clerk','male','2022-01-14','Thekkedath','kannur','taliparamba',670571,'trivandrum','clerk@gmail.com',2147483647,'kannur','kollam','Ram','Ram','Riya'),(4,'athul','male','2022-01-19','Odamvallapil','Kannur','Vellad',670571,'kannur','athul@gmail.com',2147483647,'Kannur','Taliparamba','Ramesan','Ramesan','Rathi'),(5,'Anagha','female','2021-12-31','mgfhgfhfh','sfdf','gfg',0,'kozhikode','cddd@gmail.com',0,'ewrewr','fdfd','ddddd','ssss','frgrg'),(6,'vimal','male','0000-00-00','vadiveedu','Kannur','nadiubl',33333,'Subject 2','ahh@gmail.com',588768,'kochi','taliparamba','kerala','Ramesan','Riya');

/*Table structure for table `village` */

DROP TABLE IF EXISTS `village`;

CREATE TABLE `village` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `v_name` varchar(200) DEFAULT NULL,
  `v_place` varchar(200) DEFAULT NULL,
  `v_post` varchar(200) DEFAULT NULL,
  `v_pin` int(200) DEFAULT NULL,
  `v_district` varchar(200) DEFAULT NULL,
  `v_image` varchar(200) DEFAULT NULL,
  `v_qualification` varchar(200) DEFAULT NULL,
  `v_email` varchar(200) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `v_phone` int(200) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `village` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
