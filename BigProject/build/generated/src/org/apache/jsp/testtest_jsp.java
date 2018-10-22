package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class testtest_jsp extends org.apache.jasper.runtime.HttpJspBase
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

      out.write("<!doctype html>\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("  <meta charset=\"utf-8\">\n");
      out.write("  <title>jQuery UI Tooltip - Default functionality</title>\n");
      out.write("  <link rel=\"stylesheet\" href=\"//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css\">\n");
      out.write("  <script src=\"//code.jquery.com/jquery-1.10.2.js\"></script>\n");
      out.write("  <script src=\"//code.jquery.com/ui/1.11.4/jquery-ui.js\"></script>\n");
      out.write("  <link rel=\"stylesheet\" href=\"/resources/demos/style.css\">\n");
      out.write("  <script>\n");
      out.write("  $(function() {\n");
      out.write("    $( document ).tooltip();\n");
      out.write("  });\n");
      out.write("  </script>\n");
      out.write("  <style>\n");
      out.write("  label {\n");
      out.write("    display: inline-block;\n");
      out.write("    width: 5em;\n");
      out.write("  }\n");
      out.write("  </style>\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write(" \n");
      out.write("<p><a href=\"#\" title=\"That&apos;s what this widget is\">Tooltips</a> can be attached to any element. When you hover\n");
      out.write("the element with your mouse, the title attribute is displayed in a little box next to the element, just like a native tooltip.</p>\n");
      out.write("<p>But as it's not a native tooltip, it can be styled. Any themes built with\n");
      out.write("<a href=\"http://jqueryui.com/themeroller/\" title=\"ThemeRoller: jQuery UI&apos;s theme builder application\">ThemeRoller</a>\n");
      out.write("will also style tooltips accordingly.</p>\n");
      out.write("<p>Tooltips are also useful for form elements, to show some additional information in the context of each field.</p>\n");
      out.write("<p><label for=\"age\">Your age:</label><input id=\"age\" title=\"We ask for your age only for statistical purposes.\"></p>\n");
      out.write("<p>Hover the field to see the tooltip.</p>\n");
      out.write(" \n");
      out.write(" \n");
      out.write("</body>\n");
      out.write("</html>");
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
