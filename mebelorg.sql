-- MySQL dump 10.13  Distrib 8.0.45, for macos15 (arm64)
--
-- Host: 127.0.0.1    Database: mebelorg_db
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '9e226b4a-fc0e-11f0-8207-746bb95fb055:1-233';

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `Номер_заказа` int NOT NULL,
  `Артикул_заказа` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `Дата_заказа` date NOT NULL,
  `Дата_доставки` date NOT NULL,
  `Пункт_выдачи_id` int DEFAULT NULL,
  `ФИО_клиента` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Код_для_получения` int DEFAULT NULL,
  `Статус_заказа` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`Номер_заказа`),
  KEY `Пункт_выдачи_id` (`Пункт_выдачи_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`Пункт_выдачи_id`) REFERENCES `PickupPoints` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (1,'А112Т4, 2, G843H5, 2','2024-02-27','2024-04-20',2,'Степанов Михаил Артёмович',901,'Завершен'),(2,'G843H5, 1, А112Т4, 1','2024-09-28','2024-04-21',11,'Михайлюк Анна Вячеславовна',902,'Новый'),(3,'D325D4, 10, S432T5, 10','2024-03-21','2024-04-22',2,'Ситдикова Елена Анатольевна',903,'Новый'),(4,'F325D4, 5, D325D4, 4','2024-02-20','2024-04-23',11,'Ворсин Петр Евгеньевич',904,'Завершен'),(5,'wdwfw','2026-06-01','2026-06-04',1,NULL,NULL,'Новый');
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PickupPoints`
--

DROP TABLE IF EXISTS `PickupPoints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PickupPoints` (
  `id` int NOT NULL,
  `Адрес` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PickupPoints`
--

LOCK TABLES `PickupPoints` WRITE;
/*!40000 ALTER TABLE `PickupPoints` DISABLE KEYS */;
INSERT INTO `PickupPoints` VALUES (1,'420151, г. Лесной, ул. Вишневая, 32'),(2,'125061, г. Лесной, ул. Подгорная, 8'),(3,'630370, г. Лесной, ул. Шоссейная, 24'),(4,'400562, г. Лесной, ул. Зеленая, 32'),(5,'614510, г. Лесной, ул. Маяковского, 47'),(6,'410542, г. Лесной, ул. Светлая, 46'),(7,'620839, г. Лесной, ул. Цветочная, 8'),(8,'443890, г. Лесной, ул. Коммунистическая, 1'),(9,'603379, г. Лесной, ул. Спортивная, 46'),(10,'603721, г. Лесной, ул. Гоголя, 41'),(11,'410172, г. Лесной, ул. Северная, 13'),(12,'614611, г. Лесной, ул. Молодежная, 50'),(13,'454311, г.Лесной, ул. Новая, 19'),(14,'660007, г.Лесной, ул. Октябрьская, 19'),(15,'603036, г. Лесной, ул. Садовая, 4'),(16,'394060, г.Лесной, ул. Фрунзе, 43');
/*!40000 ALTER TABLE `PickupPoints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Products` (
  `Артикул` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Наименование_товара` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `Единица_измерения` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Цена` decimal(10,2) NOT NULL,
  `Поставщик` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Производитель` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Категория_товара` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Действующая_скидка` int DEFAULT '0',
  `Кол_во_на_складе` int DEFAULT '0',
  `Описание_товара` text COLLATE utf8mb4_unicode_ci,
  `Фото` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`Артикул`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES ('1','Илья','шт',500.00,'ЗолотоеРуно','Инвуд','Прихожая',1,1,'Насрал','1.png'),('2','ывммфм','ГИ',3.00,'ЗолотоеРуно','Инвуд','Прихожая',0,1,'вЫВМЫВ',''),('C346F5','Полка настенная ромб Лофт, черная, 40 см','шт.',2843.00,'KRYLOVMANUFACTURA','RIDBERG','Полка',5,4,'Полочки для цветов в стиле лофт. Подойдут как для цветов, так и в качестве декоративного прихожей или гардеробной.','8.jpg'),('D325D4','Угловой диван Кромма Инвуд Лайт, серый двухместный диван, Velutto 32','шт.',29125.00,'Кромма','Инвуд','Диван',5,12,'Угловой диван Инвуд Лайт 2 - стильный и комфортный диван подойдет для комнаты любого размера.','3.jpg'),('F325D4','Диван, Прямой диван, Диван-кровать Сити темно-коричневый. Квест-33','шт.',14322.00,'ЗолотоеРуно','Инвуд','Диван',18,3,'Прямой диван-кровать Сити - это современное и функциональное решение для вашего дома.','5.jpg'),('G432G6','Пуф трансформер кровать раскладушка светло-коричневый велюр','шт.',6149.00,'KRYLOVMANUFACTURA','Инвуд','Пуф',22,3,'Пуф трансформер 5в1 представляет собой уникальное сочетание функций, выступая в качестве пуфика, столика, кресла, шезлонга и дополнительного спального места. ','6.jpg'),('G843H5','Прихожая в коридор Твист с зеркалом мебель со шкафами, 120х37х202 см','шт.',8803.00,'Стройландия','Мебелони','Прихожая',25,9,'Этот стеллаж со шкафом в прихожую комнату станет отличным элементом для вашего интерьера. Мебель для дома обеспечивает удобное хранение перчаток, шапок, зонтов, сумок и других аксессуаров. ','2.jpg'),('H542F5','Диван, Прямой диван, диван кровать, Рио симпл механизм Пантограф. Симпл-16','шт.',20708.00,'ЗолотоеРуно','Инвуд','Диван',4,5,'Диван Рио симпл от Золотое Руно - это сочетание комфорта, функциональности и стильного дизайна.','7.jpg'),('А112Т4','Прихожая Фаворит 1 1420х2056х352ммм Дуб Делано/Цемент Светлый SV-М 1 шт','шт.',9577.00,'Стройландия','SVМЕБЕЛЬ','Прихожая',10,0,'Удивительно функциональная и практичная прихожая Фаворит 1, обладая характерными чертами Скандинавского стиля, выглядит эффектно и способна задать тон интерьеру дома, встречая вас и ваших гостей. ','1.jpg');
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Роль_сотрудника` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ФИО` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Логин` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Пароль` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Логин` (`Логин`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Администратор','Никифорова Анна Семеновна','94d5ous@gmail.com','uzWC67'),(2,'Администратор','Стелина Евгения Петровна','uth4iz@mail.com','2L6KZG'),(3,'Администратор','Никифорова Весения Николаевна','5d4zbu@tutanota.com','rwVDh9'),(4,'Менеджер','Сазонов Руслан Германович','ptec8ym@yahoo.com','LdNyos'),(5,'Менеджер','Одинцов Серафим Артёмович','1qz4kw@mail.com','gynQMT'),(6,'Менеджер','Старикова Елена Павловна','4np6se@mail.com','AtnDjr'),(7,'Авторизированный клиент','Степанов Михаил Артёмович','yzls62@outlook.com','JlFRCZ'),(8,'Авторизированный клиент','Михайлюк Анна Вячеславовна','1diph5e@tutanota.com','8ntwUp'),(9,'Авторизированный клиент','Ситдикова Елена Анатольевна','tjde7c@yahoo.com','YOyhfR'),(10,'Авторизированный клиент','Ворсин Петр Евгеньевич','wpmrc3do@tutanota.com','RSbvHv');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-01 21:15:31
