-- Simplifico todo en una sola vista
CREATE VIEW voto_proyectos_que_pertenece AS
SELECT i.diputado_id, p.proyecto_de_ley_id, v.tipo_de_voto
FROM integrantes_comisiones i
JOIN proyectos_de_ley_comisiones p ON i.comision_id = p.comision_id
JOIN votos v ON v.ciudadano_id = i.diputado_id AND v.proyecto_de_ley_id = p.proyecto_de_ley_id;


SELECT DISTINCT c.*
FROM ciudadanos c
INNER JOIN proyectos_de_ley_por_diputado p ON c.id = p.diputado_id
WHERE c.id NOT IN (
               SELECT DISTINCT diputado_id
               FROM voto_proyectos_que_pertenece v
               WHERE v.tipo_de_voto NOT IN ('afirmativo', 'ausente')
);
