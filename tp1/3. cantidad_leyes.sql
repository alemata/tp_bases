SELECT sesiones.id, count(leyes.id) cantidad
FROM sesiones 
LEFT JOIN leyes ON sesiones.id = leyes.sesion_id
WHERE year(fecha_inicio) >= year(now()) - 2
GROUP BY sesiones.id;
