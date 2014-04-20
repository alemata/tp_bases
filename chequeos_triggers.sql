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