
def transacciones(entidad):
	transaccionessql = """

	SELECT
		en.ENTID_NombreEntidad AS "Entidad",
		cl.CLIEN_NumeroIdentificacion AS "Numero de identificacion",
		tp.TITRA_Descripcion AS "Tipo transaccion",
		mo.MONED_Codigo AS "Moneda",
		ca.CANAL_Codigo AS "Canal",
		TRANS_CLIENTExPRODUCTO "Cliente x Producto",
		TRANS_CARACTERISTICAJURISDICCION "Jurisdiccion"
		/* CLASE DE TRANSACCION NO SE TOCA */
	FROM VA_TRANSACCION tx
	INNER JOIN VA_CLIENTExPRODUCTO cxp ON cxp.CLXPR_IdInterno = tx.TRANS_CLIENTExPRODUCTO
	INNER JOIN VA_CLIENTE cl ON cl.CLIEN_idInterno = cxp.CLXPR_Cliente
	INNER JOIN KP_ENTIDAD en ON en.ENTID_idInterno = tx.TRANS_Entidad
	INNER JOIN KG_TIPOTRANSACCION tp ON tp.TITRA_IdInterno = TRANS_TipoTransaccion
	INNER JOIN KG_MONEDA mo ON mo.MONED_idInterno = tx.TRANS_Moneda
	INNER JOIN KP_CANAL ca ON ca.CANAL_idInterno = TRANS_Canal
	WHERE TRANS_Entidad = """+entidad+ """ AND
	(TRANS_Moneda = 0
	OR TRANS_Jurisdiccion = 0
	);
	"""
	return transaccionessql

def canales(entidad):
	canalsql = """
	SELECT
		en.ENTID_NombreEntidad AS "Entidad",
		cc.CARCA_Codigo AS "Caracteristica canal",
		CANAL_Codigo AS "Codigo",
		nc.NATCA_Codigo AS "Naturaleza del canal",
		tc.TITCAN_Codigo AS "Titularidad del canal"

	FROM KP_CANAL ca
	INNER JOIN KP_ENTIDAD en ON CANAL_Entidad = en.ENTID_idInterno
	INNER JOIN KG_CARACTERISTICACANAL cc ON ca.CANAL_Caracteristica = cc.CARCA_IdInterno
	INNER JOIN KG_NATURALEZACANAL nc ON ca.CANAL_Naturaleza = nc.NATCA_IdInterno
	INNER JOIN KG_TITULARIDADCANAL tc ON ca.CANAL_Titularidad = tc.TITCAN_IdInterno
	WHERE ca.CANAL_Entidad = """ +entidad+ """
	"""
	return canalsql

def asociados(entidad):
	asociadossql = """

	SELECT
		en.ENTID_NombreEntidad AS "Entidad",
		ti.TIIDE_Descripcion AS "Tipo Identificacion",
		CLIEN_NumeroIdentificacion AS "Identifiicacion",
		pe.PAIS_Nombre AS "Pais Expide Identificacion",
		tp.TIPER_Descripcion AS "Tipo de persona",
		CLIEN_Nombre1 AS "Nombre 1",
		CLIEN_Nombre2 AS "Nombre 2",
		CLIEN_Apellido1 AS "Apellido 1",
		CLIEN_Apellido2 AS "Apellido 2",
		/*CLIEN_RazonSocial,*/
		ac.ACECO_Descripcion AS "Actividad Economica",
		pn.PAIS_Nombre AS "Pais Nacimiento",
		/* oc.OCUPA_DescripcionGeneral AS "Ocupacion",*/
		pr.PAIS_Nombre AS "Pais residencia",
		te.TIEMP_Descripcion AS "Tipo de Empresa"

	FROM VA_CLIENTE cl
	INNER JOIN KG_TIPOIDENTIFICACION ti ON ti.TIIDE_IdInterno =  cl.CLIEN_TipoIdentificacion
	INNER JOIN KG_PAIS pe ON pe.PAIS_IdInterno = cl.CLIEN_PaisExpideIdentificacion
	INNER JOIN KG_TIPOPERSONA tp ON tp.TIPER_IdInterno =cl.CLIEN_TipoPersona
	INNER JOIN KG_ACTIVIDADECONOMICA ac ON ac.ACECO_IdInterno = cl.CLIEN_ActividadEconomicacliente
	INNER JOIN KG_PAIS pn ON pn.PAIS_IdInterno = cl.CLIEN_PaisNacimiento
	INNER JOIN KG_OCUPACION oc ON oc.OCUPA_IdInterno = cl.CLIEN_Ocupacion
	INNER JOIN KG_PAIS pr ON pr.PAIS_IdInterno = cl.CLIEN_PaisResidencia
	INNER JOIN KP_ENTIDAD en ON en.ENTID_idInterno = cl.CLIEN_Entidad
	INNER JOIN KG_TIPOEMPRESA te ON te.TIEMP_IdInterno = cl.CLIEN_TipoEmpresa
	WHERE CLIEN_Entidad = """ +entidad+ """ AND
	(CLIEN_TipoIdentificacion = 0
	OR CLIEN_PaisExpideIdentificacion= 0
	OR CLIEN_TipoPersona = 0
	OR CLIEN_ActividadEconomicacliente = 0
	OR CLIEN_PaisNacimiento = 0);"""
	return asociadossql

def asociados_agregado(entidad,fecha_ini,fecha_fin):
	agregado_mes = """
	select vc.CLIEN_NumeroIdentificacion as IDENTIFICACION,
	ac.ACECO_Descripcion as actividad_descripcion,
	ac.ACECO_Clase as CIIU,
	ocu.OCUPA_DescripcionGeneral,

		(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
		 from VA_TRANSACCION tr
		 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
		  where tr.TRANS_Entidad="""+entidad+""" and
		 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2
		 and tr.TRANS_FechaRealizada>'"""+fecha_ini+"""'
		 and tr.TRANS_FechaRealizada<'"""+fecha_fin+"""'

		  ) as total_debito,
		(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
		 from VA_TRANSACCION tr
		 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
		  where tr.TRANS_Entidad="""+entidad+""" and
		 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
		 and tr.TRANS_FechaRealizada>'"""+fecha_ini+"""'
		 and tr.TRANS_FechaRealizada<'"""+fecha_fin+"""'

		  ) as total_credito,
		  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
		 from VA_TRANSACCION tr
		 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
		  where tr.TRANS_Entidad="""+entidad+""" and
		 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2
		 and tr.TRANS_FechaRealizada>'"""+fecha_ini+"""'
		 and tr.TRANS_FechaRealizada<'"""+fecha_fin+"""'

		  ) as cantidad_debito,
		    (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
		 from VA_TRANSACCION tr
		 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
		  where tr.TRANS_Entidad="""+entidad+""" and
		 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
		 and tr.TRANS_FechaRealizada>'"""+fecha_ini+"""'
		 and tr.TRANS_FechaRealizada<'"""+fecha_fin+"""'

		  ) as cantidad_credito,
		  ISNULL(vc.CLIEN_MontoIngresoMensual,0) as CLIEN_MontoIngresoMensual,
		  ISNULL(vc.CLIEN_MontoOtrosIngresosMensual,0)  as CLIEN_MontoOtrosIngresosMensual,
	      ISNULL(vc.CLIEN_MontoEgresoMensual,0) as CLIEN_MontoEgresoMensual,
		  ISNULL(vc.CLIEN_MontoIngresoMensual,0) + ISNULL(vc.CLIEN_MontoOtrosIngresosMensual,0)  as CLIEN_MontoTotalIngresoMensual,
		  ISNULL(vc.CLIEN_TotalActivos,0) as CLIEN_TotalActivos,
		  ISNULL(vc.CLIEN_TotalPasivos,0) as CLIEN_TotalPasivos,
	      ISNULL(vc.CLIEN_TotalPatrimonio,0) as CLIEN_TotalPatrimonio,
		  vc.cluster as cluster_anterior,
		  vc.cluster2 as cluster_actual





     from VA_CLIENTE vc
	 inner join KG_ACTIVIDADECONOMICA ac on vc.CLIEN_ActividadEconomicacliente=ac.ACECO_IdInterno
	 inner join KG_OCUPACION ocu  on ocu.OCUPA_IdInterno = vc.CLIEN_Ocupacion
    where vc.CLIEN_Entidad="""+entidad+"""
	"""
	return agregado_mes
