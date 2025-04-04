-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS app_empresa_bd
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- Usar la base de datos
USE app_empresa_bd;

-- Eliminar la tabla 'users' si existe
DROP TABLE IF EXISTS `users`;

-- Crear la tabla 'users'
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL UNIQUE,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Eliminar la tabla 'tbl_empleados' si existe
DROP TABLE IF EXISTS `tbl_empleados`;

-- Crear la tabla 'tbl_empleados'
CREATE TABLE `tbl_empleados` (
  `CC` int NOT NULL,
  `NOM` varchar(100),
  `CAR` varchar(100),
  `CENTRO` varchar(100),
  `CASH` varchar(100),
  `SAC` varchar(100),
  `CHECK` varchar(100),
  `MOD` varchar(100),
  `ER` varchar(100),
  `PARADAS` varchar(100),
  `PERFORMANCE` varchar(100),
  PRIMARY KEY (`CC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DROP TABLE IF EXISTS `inspecciones_carretillas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspecciones_carretillas` (
  `id_inspeccion` int NOT NULL AUTO_INCREMENT,
  `placa_vehiculo` varchar(20) NOT NULL,
  `carretilla1_desgaste_llantas` enum('Si','No') NOT NULL,
  `carretilla1_daño_eje_llantas` enum('Si','No') NOT NULL,
  `carretilla1_estado_pala` enum('Si','No') NOT NULL,
  `carretilla1_estado_bastidor` enum('Si','No') NOT NULL,
  `carretilla2_desgaste_llantas` enum('Si','No') NOT NULL,
  `carretilla2_daño_eje_llantas` enum('Si','No') NOT NULL,
  `carretilla2_estado_pala` enum('Si','No') NOT NULL,
  `carretilla2_estado_bastidor` enum('Si','No') NOT NULL,
  `observaciones` text,
  `fecha_inspeccion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `inspector` varchar(100) DEFAULT NULL COMMENT 'Nombre del inspector que realizó la revisión',
  PRIMARY KEY (`id_inspeccion`),
  KEY `idx_placa` (`placa_vehiculo`),
  KEY `idx_fecha` (`fecha_inspeccion`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Registro de inspecciones de carretillas de vehículos';

DROP TABLE IF EXISTS `inspecciones_botiquines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspecciones_botiquines` (
  `id_inspeccion` int NOT NULL AUTO_INCREMENT,
  `placa_vehiculo` varchar(20) NOT NULL,
  `gasas_limpias` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `esparadrapo_tela` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `baja_lenguas` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `guantes_latex` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `venda_elastica_2` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `venda_elastica_3` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `venda_elastica_5` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `venda_algodon` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `yodopovidona` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `solucion_salina` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `termometro_digital` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `alcohol_antiseptico` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `botella_agua` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `bandas_adhesivas` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `tijeras_punta_roma` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `pito_emergencias` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `manual_primeros_auxilios` enum('CUMPLE','NO CUMPLE') NOT NULL,
  `observaciones` text,
  `fecha_inspeccion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_inspeccion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_inspeccion`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `inspeccion_cajas_fuertes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspeccion_cajas_fuertes` (
  `id_inspeccion` int NOT NULL AUTO_INCREMENT,
  `placa_vehiculo` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `puerta_estado` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `puerta_facilidad` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `clave_precisa` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `clave_autorizada` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `perilla_funciona` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `numeros_visibles` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `caja_anclada` enum('Si','No') COLLATE utf8mb4_unicode_ci NOT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `fecha_inspeccion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_inspeccion`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `tbl_conductores` (
  `id_conductor` INT NOT NULL AUTO_INCREMENT,
  `nombre_apellido` VARCHAR(50) DEFAULT NULL,
  `cedula` INT DEFAULT NULL,
  `cargo` VARCHAR(50) DEFAULT NULL,
  `vencimiento_licencia` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `dias_restantes_licencia` INT DEFAULT NULL,
  `comparendos` VARCHAR(50) DEFAULT NULL,
  `acuerdo_pago` VARCHAR(50) DEFAULT NULL,
  `vencimiento_curso` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `dias_restantes_curso` INT DEFAULT NULL,
  PRIMARY KEY (`id_conductor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
