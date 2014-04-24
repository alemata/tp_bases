SELECT DISTINCT c.*
FROM ciudadanos c
INNER JOIN voto_proyectos_que_pertenece p ON c.id = p.diputado_id
WHERE c.id NOT IN (
               SELECT DISTINCT diputado_id
               FROM voto_proyectos_que_pertenece v
               WHERE v.tipo_de_voto NOT IN ('afirmativo', 'ausente')
);
