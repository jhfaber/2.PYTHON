using System;
using System.Collections;
using System;
using System.Collections;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.HtmlControls;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Xml.Linq;
using System.Xml;
using System.Text;
using System.Security.Cryptography.X509Certificates;
using System.Net.Security;
using System.Net;
using System.IO;
using System.Reflection;
using Newtonsoft.Json;
using System.Data.SqlClient;
using System.Web.Script.Serialization;
using System.Collections.Generic;


public partial class Publico_registrar_pago : System.Web.UI.Page
{
    conexion_base db = new conexion_base();
    cookies objcookies = new cookies();
    funcionesbasicas funbas = new funcionesbasicas("", "");
    string returnValue = "";
    protected void Page_Load(object sender, EventArgs e)
    {
        Session["conf11"] = "123456789";
        Type type = typeof(Scripts_form);
        string rec = "";
        if (Request.Form.Count > 0) rec = Request.Form[0].ToString();
        carga(rec, type);
    }
    string sessionenvio = "";
    public void carga(string recibe, Type type)
    {
        try
        {

            if (recibe != "")
            {
                DataSet dts = new DataSet();

                if (Request["text_html"] != null)
                {
                    recibe = recibe.Replace("3--3", "</");
                    recibe = recibe.Replace("2**2", "/>");
                    recibe = recibe.Replace("1*-1", ">");
                    recibe = recibe.Replace("9-*9", "<");
                    //   recibe = recibe.Replace("**--**", """);
                }
                dts = funbas.JsonToTable(recibe);
                string funcion = Request["funcion"].ToString();

                if (Request["sessionenvio"] != null)
                    sessionenvio = Request["sessionenvio"].ToString();


                MethodInfo info = type.GetMethod(funcion, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
                if (info != null)
                {
                    object[] objeto2 = new object[1];
                    objeto2[0] = dts;
                    info.Invoke(this, objeto2);
                }
            }


        }
        catch (Exception ex)
        {
            returnValue = funbas.jsonerror(ex);
        }
        funbas.recogeInfoServidor(returnValue);
    }
    public void cns_consulta(DataSet ds)
    {
        try
        {
            string serial_sol_pro = ds.Tables[0].Rows[0]["serial_sol_pro"].ToString();
            DataSet dts = new DataSet();
            funcionesbasicas fn2 = new funcionesbasicas("consulta", "");
            string variable = "";
            string consulta = $@"
	            select se.serial_solreq,se.nombre,se.serial_aplicacion,se.serial_sold,se.serial_solre,se.activo 
	            from dba_solicitudes_requerimientos se
	            inner join dba_aplicaciones ap
	            on se.serial_aplicacion=ap.serial_aplicacion
	            inner join dba_solicitudes_desarrollo sd
	            on se.serial_sold=sd.serial_sold
	            inner join dba_solicitudes_requerimientos_estado sre
	            on se.serial_solre=sre.serial_solre
";
            fn2.argumentos[0] = consulta;



            fn2.Ejecutar();
            fn2.dts.Tables[0].TableName = "venta_edit";
            //fn2.dts.Tables[0].TableName = "nomuser";
            returnValue = fn2.json(fn2.dts);
        }
        catch
        {
            var s1 = new JavaScriptSerializer().Serialize(new { correcto = 0 });
            returnValue = s1.ToString();
        }
    }
}