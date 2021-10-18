CREATE SCHEMA `tutorias` ;

CREATE TABLE `tutorias`.`etapas` (
  `id_etapa` INT NOT NULL AUTO_INCREMENT,
  `etapa` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`id_etapa`)
);

CREATE TABLE `tutorias`.`preguntas` (
  `id_pregunta` INT NOT NULL AUTO_INCREMENT,
  `pregunta` VARCHAR(1000) NOT NULL,
  `respuesta` VARCHAR(10000)  NOT NULL,
  `id_etapa` INT NOT NULL,
  PRIMARY KEY (`id_pregunta`),
  FOREIGN KEY (`id_etapa`) REFERENCES etapas(`id_etapa`)
);

CREATE TABLE `tutorias`.`grado`(
`id_grado` INT NOT NULL AUTO_INCREMENT,
`semestre` VARCHAR(10) NOT NULL,
PRIMARY KEY (`id_grado`)
);

CREATE TABLE `tutorias`.`tutores` (
  `id_tutor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_tutor`)
);

CREATE TABLE `tutorias`.`alumnos` (
  `id_alumno` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80),
  `correo` VARCHAR(100),
  `id_tutor` INT NOT NULL,
  PRIMARY KEY (`id_alumno`),
  FOREIGN KEY (`id_tutor`) REFERENCES tutores(`id_tutor`)
);


CREATE TABLE `tutorias`.`preguntas_grados` (
  `id_pregunta` INT NOT NULL,
  `id_grado` INT NOT NULL,
  FOREIGN KEY (`id_pregunta`) REFERENCES preguntas(`id_pregunta`),
  FOREIGN KEY (`id_grado`) REFERENCES grado(`id_grado`)
);

INSERT INTO tutorias.tutores (nombre,correo)
VALUES ('SAMIR SARWERZIDE DE LA TORRE LEYVA','samitutorestutoresr.delatorre@academicos.udg.mx'),
       ('LAURA LÓPEZ LÓPEZ','laura.llopez@academicos.udg.mx'),
       ('PABLO SALAZAR LINARES','pablo.salazar4792@academicos.udg.mx'),
       ('JOSÉ NAVARRO RÍOS','jose.navarro1919@academicos.udg.mx'),
       ('JOSE GUADALUPE MORALES MONTELONGO','jose.gpe.morales@academicos.udg.mx'),
       ('MARCIA LETICIA MARTINEZ LARIOS','marcia.mlarios@academicos.udg.mx'),
       ('CARLOS RAMON PATIÑO RUVALCABA','carlos.patino8992@academicos.udg.mx'),
       ('CITLALLI ROSALBA RODRIGUEZ RODRIGUEZ','citalli.rodriguez@academicos.udg.mx'),
       ('NANCY RUIZ MONROY','nancy.ruiz9525@academicos.udg.mx'),
       ('JUAN CARLOS ZUÑIGA FRAGA','juan.zuniga@academicos.udg.mx'),
       ('MARTIN ANTONIO HERNANDEZ BRAVO','martin.hbravo@academicos.udg.mx'),
       ('SALVADOR CASTELLANOS PACHECO','salvador.cpacheco@academicos.udg.mx'),
       ('ÁNGELES DEL ROCIO MONTAÑEZ URIBE','angeles.montanez@academicos.udg.mx'),
       ('JOSÉ LUIS CHAVEZ VELAZQUEZ','jluis.chavez@academicos.udg.mx'),
       ('MARCO ANTONIO GONZALEZ MORALES','marco .gonzalez@academicos.udg.mx'),
       ('MARÍA TERESA DELGADO ACOSTA','mayte.delgado@academicos.udg.mx'),
       ('JOSÉ FRANCISCO JAFET, PÉREZ LÓPEZ','jfranciscojafet.perez@academicos.udg.mx'),
       ('VÍCTOR HUGO VEGA FREGOSO','victor.vega@academicos.udg.mx'),
       ('MARTHA PATRICIA BOLAÑOS DAVALOS','martha.bolanos@academicos.udg.mx'),
       ('ELIZABETH CRISTINA HERNÁNDEZ HERNÁNDEZ','elizabeth.hernandez4556@academicos.udg.mx'),
       ('JORGE LOZOYA ARANDIA','jorge.larandia@academicos.udg.mx'),
       ('MANUEL CORONA PEREZ','manuel.corona@academicos.udg.mx'),
       ('NOE ZERMEÑO MEJIA','noe.zermeno@academicos.udg.mx'),
       ('GRACIELA VILLANUEVA ALVAREZ','graciela.villanueva@academicos.udg.mx'),
       ('NOE SALVADOR HERNANDEZ GONZALEZ','noe.hernandez@academicos.udg.mx'),
       ('VIRGILIO ZUÑIGA GRAJEDA','virgilio.zuniga@academicos.udg.mx'),
       ('RIGOBERTO CÁRDENAS LARIOS','rigoberto.cardenas@academicos.udg.mx'),
       ('CARMEN JEMINA DE SANTOS ALBA','carmen.desantos@academicos.udg.mx'),
       ('CÉSAR RICARDO CORTEZ MARTINÉZ','cesar.cortez3682@academicos.udg.mx'),
       ('AARON JIMÉNEZ GOVEA','aaron.jimenez@academicos.udg.mx'),
       ('MARISELA MIRELES MERCADO','marisela.mireles@academicos.udg.mx'),
       ('CESAR ALEJANDRO GARCIA GARCIA','cesar.ggarcia@academicos.udg.mx'),
       ('MARTIN GARCIA HERNANDEZ','martin.garcia2713@academicos.udg.mx');

/*SELECT *  FROM tutores;*/

INSERT INTO tutorias.grado (semestre)
VALUES ('primero'),('segundo'),('tercero'),('cuarto'),('quinto'),('sexto'),('septimo'),('octavo'),('noveno'),('decimo');
    
/*SELECT * FROM grado;*/ 
 
INSERT INTO tutorias.etapas (etapa)
VALUES ('inicial'),('media'),('final');

/*SELECT * FROM etapas;*/

INSERT INTO tutorias.preguntas(pregunta,respuesta,id_etapa)
VALUES ('¿Cuál es el reglamento del estudiante?','REGLAMENTO ESTUDIANTE
RESPUESTA:
CON GUSTO, TE COMPARTO EL ENLACE DONDE PUEDES ENCONTRAR LA NORMATIVA GENERAL DE LA UNIVERSIDAD DE GUADALAJARA:  
http://www.cutonala.udg.mx/centro/normatividad
',1),
       ('¿Qué procede en caso de estar en artículo 34?','ARTÍCULO 34
RESPUESTA
CLARO! Aquí en este documento podrás encontrar toda la información referente al artículo 34 en las páginas 5 y 6: 
http://www.secgral.udg.mx/sites/archivos/normatividad/general/ReglamentoGralEPAlumnos.pdf
',1),
       ('¿A dónde puedo dirigirme para tramitar la credencial de estudiante? (¿Qué sucede si perdí mi credencial de estudiante?)','CREDENCIAL ESTUDIANTE
CON GUSTO TE COMPARTO EL LINK DE LA PAGINA DONDE PODRÁS REALIZAR TU TRÁMITE https://mw.siiau.udg.mx/Portal/login.xhtml ',1),
       ('¿Cuáles son los horarios de atención en el sistema de control escolar?','HORARIOS CONTROL ESCOLAR
CON GUSTO TE COMPARTO EL SIGUIENTE LINK DONDE ENCONTRARÁS LA INFORMACIÓN QUE DESEAS http://www.cutonala.udg.mx/servicios/control-escolar/contactoce ',1),
       ('¿Cómo puedo obtener el acceso a la biblioteca digital?','BIBLIOTECA DIGITAL
EN EL SIGUIENTE LINK TE COMPARTO LA INFORMACIÓN https://wdg.biblio.udg.mx/ ',1),
       ('¿Dónde puedo consultar la malla curricular?','MALLA CURRICULAR
DE ACUERDO, TE COMPARTO EL LINK DONDE ENCONTRARÁS LA MALLA DE TU CARRERA 
http://www.cutonala.udg.mx/centro/normatividad ',1),
       ('¿Dónde obtengo información sobre el centro global de idiomas?','CENTRO GLOBAL DE IDIOMAS
DE ACUERDO, TE COMPARTO EL SIGUIENTE LINK DONDE  PODRÁS ENCONTRAR LA INFORMACIÓN: http://www.cutonala.udg.mx/CGI',1),
       ('¿Cuál es el horario de atención del centro global de idiomas?','HORARIO DE CENTRO GLOBAL DE IDIOMAS
CON GUSTO TE COMPARTO LA INFORMACIÓN EN EL SIGUIENTE LINK http://www.cutonala.udg.mx/CGI',1),
       ('¿Cómo pedir las instalaciones deportivas y culturales?','INSTALACIONES DEPORTIVAS/CULTURALES
AQUÍ ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS
http://www.cutonala.udg.mx/sites/default/files/adjuntos/reglamento_para_el_uso_de_las_instalaciones_deportivas_del_centro_universitario_de_tonala_.pdf ',1),
       ('¿Cuáles son los horarios de la cineteca?','CINETECA
POR SUPUESTO, AQUÍ TIENES LA CARTELERA DE LA CINETECA: 
http://www.cutonala.udg.mx/cineclub/cartelera
',1),
       ('¿Qué requisitos se necesitan para tramitar la beca de intercambio?','BECAS INTERCAMBIO
CON GUSTO TE COMPARTO EL SIGUIENTE LINK DONDE ENCONTRARÁS EL CONTACTO PARA PEDIR INFORMACIÓN http://www.cutonala.udg.mx/servicios/servicios-academicos/unidad-becas-intercambio',2),
       ('¿En cuántas becas me puedo inscribir?','BECAS
CON GUSTO TE COMPARTO LA INFORMACIÓN, ESTAS SON LAS BECAS QUE PODRÍAS SOLICITAR
o  Apoyo alimentario: http://www.cutonala.udg.mx/becas/alimentos
o   Becarios CUT http://cutonala.udg.mx/Becarios
o   Movilidad http://cutonala.udg.mx/Becarios
',2),
       ('¿Cada cuánto tiempo se abren las convocatorias?','CONVOCATORIAS
CON GUSTO TE COMPARTO EL SIGUIENTE LINK DONDE ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/convocatorias-becas',2),
       ('¿Cómo cursó una materia en otro centro universitario?','MATERIAS EN OTRO CENTRO
RESPUESTAS:
LA INFORMACIÓN  QUE BUSCAS ESTÁ RELACIONADA CON LA SIGUIENTE INFORMACIÓN 
Movilidad http://cutonala.udg.mx/Becarios',2),
       ('Información sobre Movilidad estudiantil','MOVILIDAD ESTUDIANTIL
RESPUESTA:
CON GUSTO, LA INFORMACION QUE ESTAS BUSCANDO LA PODRÁS ENCONTRAR DE MANERA MÁS DETALLADA EN EL SIGUIENTE ENLACE:
Movilidad http://cutonala.udg.mx/Becarios
',2),
       ('¿Cuáles son las becas que puedo solicitar?','SOLICITUD DE BECAS
CON GUSTO TE COMPARTO LA INFORMACIÓN, ESTAS SON LAS BECAS QUE PODRÍAS SOLICITAR
o  Apoyo alimentario: http://www.cutonala.udg.mx/becas/alimentos
o   Becarios CUT http://cutonala.udg.mx/Becarios
o   Movilidad http://cutonala.udg.mx/Becarios',2),
       ('¿Cuándo puedo iniciar mi servicio?,¿Cuántos créditos necesito para iniciar mi servicio?','SERVICIO SOCIAL
CON GUSTO TE COMPARTO EL LINK DONDE ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/oferta-academica/salud-publica/servicio-social ',3),
       ('¿Cómo puedo realizar mi servicio social?','SERVICIO SOCIAL
CON GUSTO TE COMPARTO EL LINK DONDE ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/oferta-academica/salud-publica/servicio-social',3),
       ('¿Cuál es el proceso de titulación?','TITULACIÓN
EN ESTE LINK ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/sites/default/files/adjuntos/reglamento_de_titulacion_del_centro_universitario_de_tonala.pdf ',3),
       ('¿A partir de cuándo puedo iniciar el proceso de titulación?','TITULACIÓN
EN ESTE LINK ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/sites/default/files/adjuntos/reglamento_de_titulacion_del_centro_universitario_de_tonala.pdf ',3),
       ('¿Cuáles son las modalidades de titulación? ¿Qué hago si ya terminé mis créditos?','MODALIDADES TITULACIÓN
EN ESTE LINK ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/sites/default/files/adjuntos/reglamento_de_titulacion_del_centro_universitario_de_tonala.pdf',3),
       ('¿Cuál es el reglamento general de titulación?','REGLAMENTO TITULACIÓN
EN ESTE LINK ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.secgral.udg.mx/sites/archivos/normatividad/general/ReglamentoGeneraldeTitulacion.pdf ',3),
       ('¿Quién me puede ayudar en mi tesis? ','ASESOR TESIS
EN ESTE LINK ENCONTRARÁS LA INFORMACIÓN QUE NECESITAS http://www.cutonala.udg.mx/sites/default/files/adjuntos/reglamento_de_titulacion_del_centro_universitario_de_tonala.pdf',3);
  
SELECT * FROM preguntas_grados;