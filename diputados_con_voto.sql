#Dame todos los diputados tal que no exista un voto para ese diputado de tipo ... para 
#un proyecto de ley que sea estudiado por la comision que integra
SELECT *
FROM diputados d
WHERE NOT EXISTS
	(SELECT *
	FROM votos
	WHERE votos.ciudadano_id = d.id AND
	votos.tipo_de_voto NOT IN ('afirmativo', 'ausente')
	AND 
	votos.proyecto_de_ley_id IN (
		SELECT proyecto_de_ley_id 
		FROM integrantes_comisiones i
		JOIN proyectos_de_ley_comisiones p ON i.comision_id = p.comision_id
		WHERE i.diputado_id = d.id
	)
) 
AND EXISTS
	(SELECT *
	FROM votos
	WHERE votos.ciudadano_id = d.id
	AND 
	votos.proyecto_de_ley_id IN (
		SELECT proyecto_de_ley_id 
		FROM integrantes_comisiones i
		JOIN proyectos_de_ley_comisiones p ON i.comision_id = p.comision_id
		WHERE i.diputado_id = d.id
	)
);
  
  