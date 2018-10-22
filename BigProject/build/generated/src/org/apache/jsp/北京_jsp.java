package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class 北京_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List<String> _jspx_dependants;

  private org.glassfish.jsp.api.ResourceInjector _jspx_resourceInjector;

  public java.util.List<String> getDependants() {
    return _jspx_dependants;
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;

    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;
      _jspx_resourceInjector = (org.glassfish.jsp.api.ResourceInjector) application.getAttribute("com.sun.appserv.jsp.resource.injector");

      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE html>\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n");
      out.write("        <link rel=\"stylesheet\" href=\"https://cache.amap.com/lbs/static/main1119.css\"/>\n");
      out.write("    <script src=\"https://webapi.amap.com/maps?v=1.4.10&key=69c70ee2c4d2e932f9a8b4ac0b5afb29\"></script>\n");
      out.write("        <title>JSP Page</title>\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("       <div id=\"container\"></div>\n");
      out.write("\n");
      out.write("<script>\n");
      out.write("\n");
      out.write("var map = new AMap.Map('container', {\n");
      out.write("        resizeEnable: true,\n");
      out.write("        zoom:11,\n");
      out.write("        center: [116.397428, 39.90923]\n");
      out.write(" });\n");
      out.write(" var heatmap;\n");
      out.write(" var points =[\n");
      out.write("        {\"lng\":116.191031,\"lat\":39.988585,\"count\":10000},\n");
      out.write("        {\"lng\":116.389275,\"lat\":39.925818,\"count\":10000}, \n");
      out.write("        {\"lng\":116.287444,\"lat\":39.810742,\"count\":12000},\n");
      out.write("        {\"lng\":116.481707,\"lat\":39.940089,\"count\":13000},\n");
      out.write("        {\"lng\":116.410588,\"lat\":39.880172,\"count\":14000},\n");
      out.write("        {\"lng\":116.394816,\"lat\":39.91181,\"count\":15000},\n");
      out.write("        {\"lng\":116.416002,\"lat\":39.952917,\"count\":16000}\n");
      out.write("    ];\n");
      out.write("    map.plugin([\"AMap.Heatmap\"],function() {      //加载热力图插件\n");
      out.write("        heatmap = new AMap.Heatmap(map,{\n");
      out.write("\t\t\tradius:50,  //给定半径\n");
      out.write("\t\t\topacity: [0,0.8]\n");
      out.write("\t\t});    //在地图对象叠加热力图\n");
      out.write("        heatmap.setDataSet({\n");
      out.write("\t\tdata:points,\n");
      out.write("\t\tmax:100\n");
      out.write("\t\t}); //设置热力图数据集\n");
      out.write("        //具体参数见接口文档\n");
      out.write("    }); \n");
      out.write(" </script>\n");
      out.write("</body>\n");
      out.write("</html>\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          out.clearBuffer();
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
