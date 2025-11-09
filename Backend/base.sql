-- Active: 1762726616434@@mysql-tomasmaraval.alwaysdata.net@3306
SHOW DATABASES;
use tomasmaraval_familybank;

SELECT * FROM usuarios

SELECT * FROM actividades

SELECT * FROM solicitudes

/* */

/*
INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Tomas', 'Maraval', 123456, True, 100000, 'AguanteCentral1!', 'tomimaraval', True, 'foto.jpg');

INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Felicitas', 'Orlando Linares', 654321, True, 500000, 'Linares123!', 'felicitasorlando', True, 'imagen.jpg');

INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Maria Valentina', 'Morello', 123654, True, 1000000, 'Vmorello234!', 'valentina.morello', True, 'fotodeperfil.jpg');
*/

/* AGREGADO DE HIJOS 
INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Sol', 'Morello', 123654, False, 10, 'Sol1!', 'solmorello', True, '"/Images/fotos_de_perfil/fotosol.jpg"'),
(Null, 'Juana', 'Morello', 123654, False, 99999, 'Juanita01!', 'juanimorello', True, '"/Images/fotos_de_perfil/fotojuani.jpg"');

INSERT INTO `usuarios`(`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`)
VALUES (Null, 'Juan', 'Maraval', 123456, False, 100, 'JuanMar12', 'juanmaraval', True, '"/Images/fotos_de_perfil/fotojuan.jpg"'),
(Null, 'Maria', 'Maraval', 123456, False, 10000, 'Maru123', 'marumar', True, '"/Images/fotos_de_perfil/fotomaria.jpg"');
 
INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Nicolas', 'Orlando Linares', 654321, False, 100, 'Nico0090605', 'nico.ol', True, '"/Images/fotos_de_perfil/fotonico.jpg"'), 
(Null, 'Violeta', 'Orlando Linares', 654321, False, 1000, 'Viole23', 'violeorlando', True, '"/Images/fotos_de_perfil/fotovilu.jpg"');
*/

/* MOSTRAR POR FAMILIA*/

SELECT * FROM usuarios WHERE `codigo_Familiar`= 654321

SELECT * FROM usuarios WHERE `codigo_Familiar`= 123456

SELECT * FROM usuarios WHERE `codigo_Familiar`= 123654


/*MOSTRAR USUARIOS ADMINISTRADORES*/
SELECT * FROM usuarios where es_padre= TRUE;


/* actividades */

INSERT into `actividades` (`id`, `emisor`, `receptor`, `motivo`, `fecha`, `monto`) VALUES (Null, 2, 6, 'Pago uber', '2025-11-03T10:43', 25000), 
(Null, 1, 3, 'Compra Starbucks Iced Vanilla Latte Macchiatto with whipped cream honey mustard', '2025-11-01T00:49', 2314567865432), 
(Null, 3, 10, 'Entradas', '2025-11-03T10:43', 10000), 
(Null, 2, 11, 'Vario', '2025-11-03T10:43', 5000)


/* actividades por emisor*/

SELECT emisor.nombre_usuario AS Emisor,  receptor.nombre_usuario AS Receptor,
actividades.monto AS Monto, actividades.motivo as Motivo, actividades.fecha as Fecha FROM actividades
INNER JOIN usuarios AS emisor ON actividades.emisor = emisor.id
INNER JOIN usuarios AS receptor ON actividades.receptor = receptor.id
WHERE emisor.id = 2

/*ULTIMAS ACTIVIDADES REGISTRADAS*/
SELECT emisor.nombre_usuario AS Emisor, receptor.nombre_usuario AS Receptor, actividades.motivo, actividades.monto, actividades.fecha
FROM actividades 
INNER JOIN usuarios as emisor  ON actividades.emisor = emisor.id
INNER JOIN usuarios as receptor ON actividades.receptor = receptor.id
ORDER BY actividades.fecha DESC
LIMIT 5;

/*SOLICITUDES*/

INSERT INTO `solicitudes` (`id`, `id_usuario`, `monto`, `fecha`, `estado`) 
VALUES (Null, 12, 10000, '2025-11-03T10:43', 'pendiente'),
(Null, 14, 50000, '2025-11-03T10:43', 'pendiente'),
(Null, 10, 500000, '2025-11-03T10:43', 'pendiente'),
(Null, 10, 1200, '2025-11-09T19:43', 'pendiente');

/*CONTAR SOLICITUDES*/
SELECT usuarios.nombre_usuario AS usuario, COUNT(solicitudes.id) AS cantidad_de_solicitudes
FROM usuarios
INNER JOIN solicitudes ON usuarios.id = solicitudes.id_usuario
GROUP BY usuarios.id, usuarios.nombre_usuario;

/*SOLICITUDES PENDIENTES*/
SELECT solicitudes.id, usuarios.nombre_usuario, solicitudes.monto, solicitudes.fecha, solicitudes.estado
FROM solicitudes
INNER JOIN usuarios ON solicitudes.id_usuario = usuarios.id
WHERE solicitudes.estado = 'pendiente';

