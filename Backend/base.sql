-- Active: 1761576574446@@mysql-tomasmaraval.alwaysdata.net@3306@tomasmaraval_familybank
SHOW DATABASES;
use tomasmaraval_familybank;

SET time_zone = 'America/Buenos_Aires';

SELECT * FROM usuarios

SELECT * FROM actividades

SELECT * FROM solicitudes


INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Tomas', 'Maraval', 123456, True, 100000, 'AguanteCentral1!', 'tomimaraval', True, 'foto.jpg');

INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Felicitas', 'Orlando Linares', 654321, True, 500000, 'Linares123!', 'felicitasorlando', True, 'imagen.jpg');

INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Maria Valentina', 'Morello', 123654, True, 1000000, 'Vmorello234!', 'valentina.morello', True, 'fotodeperfil.jpg');


/* AGREGADO DE HIJOS */
INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Sol', 'Morello', 123654, False, 10, 'Sol1!', 'solmorello', True, '"/Images/fotos_de_perfil/fotosol.jpg"'),
(Null, 'Juana', 'Morello', 123654, False, 99999, 'Juanita01!', 'juanimorello', True, '"/Images/fotos_de_perfil/fotojuani.jpg"');

INSERT INTO `usuarios`(`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`)
VALUES (Null, 'Juan', 'Maraval', 123456, False, 100, 'JuanMar12', 'juanmaraval', True, '"/Images/fotos_de_perfil/fotojuan.jpg"'),
(Null, 'Maria', 'Maraval', 123456, False, 10000, 'Maru123', 'marumar', True, '"/Images/fotos_de_perfil/fotomaria.jpg"');
 
INSERT INTO `usuarios` (`id`, `nombres`, `apellido`, `codigo_Familiar`, `es_padre`, `saldo`,  `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
VALUES (Null, 'Nicolas', 'Orlando Linares', 654321, False, 100, 'Nico0090605', 'nico.ol', True, '"/Images/fotos_de_perfil/fotonico.jpg"'), 
(Null, 'Violeta', 'Orlando Linares', 654321, False, 1000, 'Viole23', 'violeorlando', True, '"/Images/fotos_de_perfil/fotovilu.jpg"');


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


/*Buscar usuario y contrasenia PARA LOGIN*/
select nombre_usuario, contrasenia from usuarios where nombre_usuario = 'solmorello' and contrasenia = 'Sol1!'

/*Crear usuarios para REGISTRO*/
insert into usuarios (`id`, `nombres`, `apellido`, `codigo_familiar`, `es_padre`, `saldo`, `contrasenia`, `nombre_usuario`, `admitido`, `img`) 
values (null, 'Juan Ramon', 'Ramirez', 999999, 1, 0, 'juanRa02.', 'juanRamirez', 1, 'Frontend/Images/user.pmg')

/*Modificar saldos para TRANSFERENCIA o INGRESOS*/
update usuarios set saldo = 100000 where id = 16 

/*Modificar datos del usuario*/
update usuarios set nombres = 'Juana Ramona', apellido = 'Di Maria' where id = 16 ;

/*Crear actividades*/
insert into actividades (`id`, `emisor`, `receptor`, `motivo`, `fecha`, `monto`) 
values (Null, 16, 2, 'Coima', now(), 10)

/*Crear solicitudes*/
insert into solicitudes (`id`, `id_usuario`, `monto`, `fecha`, `estado`) 
values (Null, 12, 10000, now(), 'pendiente'),

/*Ver actividades de x persona*/
select receptor.nombre_usuario as usuario, receptor.nombres as nombre, motivo, monto, fecha
from actividades 
inner join usuarios as receptor on actividades.receptor = receptor.id
where emisor = 16 order by fecha desc

/*Ver nombre_usuario*/
select nombre_usuario from usuarios where id = 1

/*Ver codigo familiar*/
select codigo_familiar from usuarios where id = 1

/*Ver nombre_usuario*/
select nombre_usuario from usuarios where id = 1

/*Crear solicitudes*/
insert into solicitudes (`id`, `id_usuario`, `monto`, `fecha`, `estado`) 
values (null, 11, 20, now(), 'pendiente')

/*Ver solicitudes de grupo familiar*/
select monto, estado, fecha, usuarios.codigo_familiar as familia, usuarios.nombres as hijo from solicitudes
inner join usuarios on solicitudes.id_usuario = usuarios.id
where usuarios.codigo_familiar = 123654 order by fecha asc ;


/*Ver hijos aun por admitir (por ID)*/
SELECT padre.nombre_usuario as PADRE, hijos.nombre_usuario as username, hijos.nombres as Nombre, hijos.apellido as Apellido 
FROM usuarios padre, usuarios hijos
WHERE padre.es_padre = 1 AND hijos.es_padre = 0 AND padre.codigo_Familiar = hijos.codigo_Familiar 
    AND hijos.admitido = 0 AND padre.id=3;

/*Aceptar hijos*/
UPDATE usuarios SET admitido = 1 WHERE usuarios.id = 10 AND usuarios.es_padre = 0;


/*Monto total solicitasdo por hijo*/
SELECT usuarios.nombres AS Nombres, SUM(solicitudes.monto) AS MontoTotal, COUNT(solicitudes.monto) AS Solicitudes
FROM usuarios
INNER JOIN solicitudes ON solicitudes.id_usuario = usuarios.id
GROUP BY usuarios.nombres
HAVING usuarios.nombres ='Juana';


-- Borrar NO TOCAR --
DELETE * FROM solicitudes 
WHERE id_usuario = 15 AND estado = 'pendiente' 

