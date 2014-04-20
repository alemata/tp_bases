# Probando con otra cosita desde el primero
SELECT c.*, (df.patrimonio / di.patrimonio - 1) * 100 incremento_porcentual
FROM declaraciones_juradas di
INNER JOIN ciudadanos c ON c.id = di.ciudadano_id
INNER JOIN declaraciones_juradas df ON di.ciudadano_id = df.ciudadano_id
WHERE df.año = (
	SELECT MAX(año) 
	FROM declaraciones_juradas dj 
	WHERE dj.ciudadano_id = di.ciudadano_id)
GROUP BY di.ciudadano_id
ORDER BY di.año ASC;
