DELIMITER $$
 
CREATE TRIGGER chequear_edad_diputados
     BEFORE INSERT ON diputados FOR EACH ROW
     BEGIN
          IF (SELECT edad FROM ciudadanos WHERE id = NEW.id) < 25 THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No se puede ser diputado con esa edad';
     	END IF;
     END;
$$

DELIMITER $$ 
 
CREATE TRIGGER chequear_edad_senadores
     BEFORE INSERT ON representaciones FOR EACH ROW
     BEGIN
          IF NEW.camara_id = 'senadores' AND (SELECT edad FROM ciudadanos WHERE id = NEW.ciudadano_id) < 30 THEN 
     		SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'No se puede ser senador con esa edad';
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



