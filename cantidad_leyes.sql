(SELECT sesiones.id, count(*)
FROM sesiones INNER JOIN leyes ON sesiones.id = leyes.sesion_id
WHERE year(fecha_inicio) >= year(now()) - 2
GROUP BY sesiones.id)
UNION 
(SELECT sesiones.id, 0
FROM sesiones LEFT JOIN leyes ON sesiones.id = leyes.sesion_id
WHERE leyes.id is NULL
AND year(fecha_inicio) >= year(now()) - 2
GROUP BY sesiones.id)