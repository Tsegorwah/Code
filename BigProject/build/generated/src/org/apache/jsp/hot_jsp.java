package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class hot_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      response.setContentType("text/html");
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
      out.write("<!DOCTYPE html>\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n");
      out.write("\t<meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=no\" />\n");
      out.write("\t<style type=\"text/css\">\n");
      out.write("\t#allmap {width:100%;height: 800px;overflow: hidden;margin:0;font-family:\"????\";}\n");
      out.write("\t</style>\n");
      out.write("\t<script type=\"text/javascript\" src=\"http://api.map.baidu.com/api?v=2.0&ak=X7gAHGornMEjuZgXXVcp3P3AcWDgloGL\"></script>\n");
      out.write("\t<title>hot</title>\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("\t<div id=\"allmap\"></div>\n");
      out.write("</body>\n");
      out.write("</html>\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("\t// ????API??\n");
      out.write("\tvar map = new BMap.Map(\"allmap\");    // ??Map??\n");
      out.write("\tmap.centerAndZoom(new BMap.Point(116.404, 39.915), 11);  // ?????,????????????\n");
      out.write("\t//????????\n");
      out.write("\tmap.addControl(new BMap.MapTypeControl({\n");
      out.write("\t\tmapTypes:[\n");
      out.write("            BMAP_NORMAL_MAP,\n");
      out.write("            BMAP_HYBRID_MAP\n");
      out.write("        ]}));\t  \n");
      out.write("\tmap.setCurrentCity(\"??\");          // ????????? ????????\n");
      out.write("\tmap.enableScrollWheelZoom(true);     //????????\n");
      out.write("</script>\n");
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
