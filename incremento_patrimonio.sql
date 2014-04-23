SELECT c.id, c.nombre, c.apellido,
      IF (dji.patrimonio = 0, 100, (djf.patrimonio / dji.patrimonio - 1) * 100) incremento_porcentual
FROM declaraciones_juradas dji
INNER JOIN ciudadanos c ON c.id = dji.ciudadano_id
INNER JOIN declaraciones_juradas djf ON dji.ciudadano_id = djf.ciudadano_id
WHERE djf.año = (
  SELECT MAX(año)
  FROM declaraciones_juradas dj
  WHERE dj.ciudadano_id = c.id)
AND dji.año = (
  SELECT MIN(año)
  FROM declaraciones_juradas dj
  WHERE dj.ciudadano_id = c.id)
ORDER BY incremento_porcentual DESC
LIMIT 10;
