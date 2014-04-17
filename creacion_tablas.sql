#Camaras
CREATE TABLE camaras (
	id INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id)
 );
 
CREATE TABLE camara_senadores (
	id INT NOT NULL,
	PRIMARY KEY (id),
 	FOREIGN KEY (id) REFERENCES camaras(id) 
 );
 
 CREATE TABLE camara_diputados (
 	id INT NOT NULL,
 	PRIMARY KEY (id),
 	FOREIGN KEY (id) REFERENCES camaras(id) 
 );
 
 #Ciudadanos
 CREATE TABLE ciudadanos (
	id INT NOT NULL AUTO_INCREMENT,
	dni VARCHAR(10),
	edad INT,
	nombre VARCHAR(100),
	apellido VARCHAR(100),
	PRIMARY KEY (id)
 );
 
 CREATE TABLE diputados (
	id INT NOT NULL,	
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES ciudadanos(id) 
 );
 
 CREATE TABLE empleados (
	id INT NOT NULL,	
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES ciudadanos(id) 
 );  
 
 #Provincia
 CREATE TABLE provincias (
	id INT NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(100),
	poblacion INT,
	PRIMARY KEY (id)
 );
 
  
 #Ternaria entre camara, ciudadano y provincia
 CREATE TABLE representaciones (
	ciudadano_id INT NOT NULL,
	camara_id INT NOT NULL,
	provincia_id INT NOT NULL,
	año INT NOT NULL,
	PRIMARY KEY (ciudadano_id, camara_id, provincia_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (camara_id) REFERENCES camaras(id),
	FOREIGN KEY (provincia_id) REFERENCES provincias(id)
 );
 
 
 #Relacion entre camara y ciudadanos
 CREATE TABLE presidentes_camaras (
	ciudadano_id INT NOT NULL,
	camara_id INT NOT NULL,
	año INT NOT NULL, 
	PRIMARY KEY (ciudadano_id, camara_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (camara_id) REFERENCES camaras(id)
 );
 
 #-------------------------------------------------------------#
 
 #Bloque politico
 CREATE TABLE bloques_politicos (
	id INT NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(100),
	PRIMARY KEY (id)
 );
 
 #Bloque politico con ciudadadnos (presidentes)
 CREATE TABLE bloques_politicos_ciudadanos_presidentes (
	ciudadano_id INT NOT NULL,
	bloque_politico_id INT NOT NULL,
	año INT,
	PRIMARY KEY (ciudadano_id, bloque_politico_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (bloque_politico_id) REFERENCES bloques_politicos(id) 
 );
 
  #Bloque politico con ciudadadnos (integrantes)
 CREATE TABLE bloques_politicos_ciudadanos_inegrantes (
	ciudadano_id INT NOT NULL,
	bloque_politico_id INT NOT NULL,
	año INT,
	PRIMARY KEY (ciudadano_id, bloque_politico_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (bloque_politico_id) REFERENCES bloques_politicos(id) 
 );
 

 #-------------------------------------------------------------#
 
 #Partido politico
 CREATE TABLE partidos_politicos (
	id INT NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(100),
	PRIMARY KEY (id)
 );
 
 #Partido politico con ciudadadnos
 CREATE TABLE partidos_politicos_ciudadanos (
	ciudadano_id INT NOT NULL,
	partido_politico_id INT NOT NULL,
	año INT,
	PRIMARY KEY (ciudadano_id, partido_politico_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (partido_politico_id) REFERENCES partidos_politicos(id) 
 );
 
  #-------------------------------------------------------------#
  
 #Bienes economicos
 CREATE TABLE bienes_economicos (
	id INT NOT NULL AUTO_INCREMENT,
	valor INT,
	PRIMARY KEY (id)
 );
 
 #Bienes con ciudadanos
 CREATE TABLE bienes_economicos_ciudadanos (
  	bien_economico_id INT NOT NULL,
	ciudadano_id INT NOT NULL,
	año INT,
	PRIMARY KEY (ciudadano_id, bien_economico_id, año),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (bien_economico_id) REFERENCES bienes_economicos(id) 
 );
  
 
  #-------------------------------------------------------------# 
  
 #Sesion
 CREATE TABLE sesiones (
  	id INT NOT NULL AUTO_INCREMENT,
	fecha_inicio date,
	fecha_fin date,
	camara_id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (camara_id) REFERENCES camaras(id)
 );

#Control
CREATE TABLE controles (
	id INT NOT NULL AUTO_INCREMENT,
	empleado_id INT,
	PRIMARY KEY (id),
	FOREIGN KEY (empleado_id) REFERENCES empleados(id)
 );
  
  
 #Proyecto de ley
 CREATE TABLE proyectos_de_ley (
  	id INT NOT NULL AUTO_INCREMENT,
	fecha_inicio DATE,
	camara_id INT NOT NULL,
	titulo VARCHAR(100),
	control_id INT, #aclara que se controla cada proyecto como mucho una vez
	PRIMARY KEY (id),
	FOREIGN KEY (camara_id) REFERENCES camaras(id),
	FOREIGN KEY (control_id) REFERENCES controles(id)
 );  
  
#Ley
 CREATE TABLE leyes (
  	id INT NOT NULL AUTO_INCREMENT,
	año INT,
	sesion_id INT NOT NULL,
	proyecto_de_ley_id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (sesion_id) REFERENCES sesiones(id),
	FOREIGN KEY (proyecto_de_ley_id) REFERENCES proyectos_de_ley(id)
 );
 
#TipoVoto
 CREATE TABLE tipos_de_voto (
  	id INT NOT NULL AUTO_INCREMENT,
	tipo VARCHAR(100),
	PRIMARY KEY (id)	
 );
 
 #Ternaria entre ciudadano, sesion y proyecto de ley
 CREATE TABLE voto (
	ciudadano_id INT NOT NULL,
	sesion_id INT NOT NULL,
	proyecto_de_ley_id INT NOT NULL,
	tipo_de_voto_id INT,
	#deshabilitado TINYINT(1), #Boolean value: 1 for true 0 for false
	PRIMARY KEY (ciudadano_id, sesion_id, proyecto_de_ley_id), #Va la sesion como PK? No es 1 la cardinalidad de sesion?
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (sesion_id) REFERENCES sesiones(id),
	FOREIGN KEY (proyecto_de_ley_id) REFERENCES proyectos_de_ley(id)
 );


#Comision
 CREATE TABLE comisiones (
  	id INT NOT NULL AUTO_INCREMENT,
	nombre VARCHAR(100),
	PRIMARY KEY (id)	
 );
 
 #Diputados con comisiones (pertenece)
  CREATE TABLE integrantes_comisiones (
	diputado_id INT NOT NULL,
	comision_id INT NOT NULL,
	año INT,
	PRIMARY KEY (diputado_id, comision_id, año),
	FOREIGN KEY (diputado_id) REFERENCES diputados(id),
	FOREIGN KEY (comision_id) REFERENCES comisiones(id) 
 );
 
  #Diputados con comisiones (presidente)
  CREATE TABLE presidentes_comisiones (
	diputado_id INT NOT NULL,
	comision_id INT NOT NULL,
	año INT,
	PRIMARY KEY (diputado_id, comision_id, año),
	FOREIGN KEY (diputado_id) REFERENCES diputados(id),
	FOREIGN KEY (comision_id) REFERENCES comisiones(id) 
 );


  #Proyectos de ley con comisiones
  CREATE TABLE proyectos_de_ley_comisiones (
	proyecto_de_ley_id INT NOT NULL,
	comision_id INT NOT NULL,
	diputado_id INT,
	PRIMARY KEY (proyecto_de_ley_id, comision_id),
	FOREIGN KEY (proyecto_de_ley_id) REFERENCES proyectos_de_ley(id),
	FOREIGN KEY (comision_id) REFERENCES comisiones(id),
	FOREIGN KEY (diputado_id) REFERENCES diputados(id)  
 );
 
  
CREATE TABLE  camara_diputados_comisiones(
	camara_diputados_id INT NOT NULL,
	comision_id INT NOT NULL,
	año INT,
	PRIMARY KEY (camara_diputados_id, comision_id, año),
	FOREIGN KEY (camara_diputados_id) REFERENCES camara_diputados(id),
	FOREIGN KEY (comision_id) REFERENCES comisiones(id) 
 );
  
#Relacion ciudadanos sesiones (asistencias) 
CREATE TABLE  asistencias(
	ciudadano_id INT NOT NULL,
	sesion_id INT NOT NULL,
	PRIMARY KEY (ciudadano_id, sesion_id),
	FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
	FOREIGN KEY (sesion_id) REFERENCES sesiones(id) 
 );
  
  