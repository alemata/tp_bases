DELIMITER $$
 
CREATE TRIGGER chequear_edad_diputados
     BEFORE INSERT ON diputados FOR EACH ROW
     BEGIN
          IF (year(now()) - (SELECT year(fecha_nacimiento) FROM ciudadanos WHERE id = NEW.id)) < 25 THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No se puede ser diputado con esa edad';
     	END IF;
     END;
$$

DELIMITER $$ 
 
CREATE TRIGGER chequeo_representaciones
     BEFORE INSERT ON representaciones FOR EACH ROW
     BEGIN
        IF NEW.camara_id = 'senadores' AND 
           (year(now()) - (SELECT year(fecha_nacimiento) FROM ciudadanos WHERE id = NEW.ciudadano_id)) < 30 THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No se puede ser senador con esa edad';
     	END IF;
     	
     	IF EXISTS (SELECT id 
				   FROM representaciones 
				   INNER JOIN camaras ON representaciones.camara_id = camaras.id 
                   WHERE ciudadano_id = NEW.ciudadano_id AND 
                   año = (SELECT año FROM camaras WHERE id = NEW.camara_id) 
                   ) THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Solo puede estar en una camara para un mismo año';
     	END IF;
     	
     END;
$$

DELIMITER $$

CREATE TRIGGER chequear_edad_ciudadanos
	BEFORE INSERT ON ciudadanos FOR EACH ROW
	BEGIN
		IF (year(now()) - year(NEW.fecha_nacimiento)) < 18 THEN 
			SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No puede ingresar un ciudadano menor a 18 años';
		END IF;
		
	END;
$$

DELIMITER $$

CREATE TRIGGER no_agregar_asistencia_si_voto_ausente
     BEFORE INSERT ON asistencias FOR EACH ROW
     BEGIN
          IF (SELECT count(*) 
          		FROM votos 	
          		WHERE ciudadano_id = NEW.ciudadano_id AND
          		sesion_id = NEW.sesion_id AND
          		tipo_de_voto = 'ausente' 
              ) > 0 THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Hay un voto ausente para ese ciudadano en esa sesion';
     	END IF;
     END;
$$

DELIMITER $$

CREATE TRIGGER no_agregar_voto_ausente_si_asistencia
     BEFORE INSERT ON votos FOR EACH ROW
     BEGIN
          IF (NEW.tipo_de_voto = 'ausente' AND
             (SELECT count(*) 
          		FROM asistencias 	
          		WHERE ciudadano_id = NEW.ciudadano_id AND
          		sesion_id = NEW.sesion_id
              ) > 0) THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No se puede agregar un voto ausente porque hay datos que verifican que el legislador estuvo presente en esa sesion';
     	END IF;
     END;
$$


DELIMITER $$ 
 
CREATE TRIGGER chequear_ley_aprobada_en_ambas_camaras
     BEFORE INSERT ON leyes FOR EACH ROW
     BEGIN
        IF (EXISTS
        		(SELECT id FROM proyectos_de_ley 
        				   WHERE id = NEW.proyecto_de_ley_id AND
        				   (aprobado_diputados = 0 OR
        				   aprobado_senadores = 0)
        		)
        	)THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No esta aprobado el proyecto en ambas camaras';
     	END IF;
     	
     END;
$$