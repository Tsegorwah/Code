package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class luntan_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("        <title>JSP Page</title>\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <div id=\"lt\">\n");
      out.write("            <table align=\"center\" class=\"hovertable\">\n");
      out.write("<tr height=\"120\">\n");
      out.write("    <th colspan=\"5\"><input class=\"ltbt\" type=\"button\" name=\"Submit\" title=\"发帖\" onclick=\"location.href='reg.jsp'\"/> \n");
      out.write("    <input class=\"ltbt\" type=\"button\" name=\"Submit\" title=\"查看热力图\"  v-on:click=\"hotblock()\"/>\n");
      out.write("    <input class=\"ltbt\" type=\"button\" name=\"Submit\" title=\"查看我的贴子\" onclick=\"location.href='reg.jsp'\"/>\n");
      out.write("    <input class=\"ltbt\" type=\"button\" name=\"Submit2\" title=\"修改热力信息\" onclick=\"location.href='reg.jsp'\"/>\n");
      out.write("    <input class=\"ltbt\" type=\"button\" name=\"Submit2\" title=\"热帖\" onclick=\"location.href='reg.jsp'\"/></th>\n");
      out.write("    \n");
      out.write("  </tr>\n");
      out.write("<tr height=\"90\">\n");
      out.write("    <td width=\"50%\" ><div align=\"center\" class=\"STYLE1\">标题</div></td>\n");
      out.write("    <td width=\"20%\" ><div align=\"center\" class=\"STYLE1\">作者</div></td>\n");
      out.write("    <td width=\"20%\" ><div align=\"center\" class=\"STYLE1\">发表日期</div></td>\n");
      out.write("    <td width=\"10%\"><div align=\"center\" class=\"STYLE1\">回复数</div></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<td height=\"22\"></td><td></td><td></td><td></td>\n");
      out.write("</tr>\n");
      out.write("<tr class=\"yellow\">\n");
      out.write("\t<th colspan=\"4\">翻页</th>\n");
      out.write("</tr>\n");
      out.write("</table>\n");
      out.write("        </div>\n");
      out.write("    </body>\n");
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
