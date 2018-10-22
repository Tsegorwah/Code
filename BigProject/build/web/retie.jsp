<%-- 
    Document   : retie
    Created on : 2018-10-17, 9:06:25
    Author     : yyznb
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
       <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link href="css/mapcss.css" rel="stylesheet" type="text/css"/>
         <script type="text/javascript" src="js/vue.js"></script>
          <script src="https://webapi.amap.com/maps?v=1.4.10&key=69c70ee2c4d2e932f9a8b4ac0b5afb29"></script>
          <script type="text/javascript" src="js/1.9.1jquery.min.js"></script>
          <script type="text/javascript" src="js/jquery-ui.min.js"></script>
          <script>
            $(function() {
    $( document ).tooltip();
  });</script>
        <title>JSP Page</title>
    </head>
    <body>
  <jsp:include flush="true" page="head.jsp"></jsp:include>
        <div id="rt">
            <table align="center" class="hovertable">
<tr height="150">
    <th colspan="5">  
    <input id="fanhui" type="button" name="Submit" title="返回首页" onclick="location.href='index.jsp'"/>
    <div class="city">热帖</div></th>  </th>  
  </tr>
<tr height="90">
    <td width="50%" id="noborder"><div align="center" class="STYLE1">标题</div></td>
    <td width="20%" id="noborder"><div  class="STYLE1">作者</div></td>
    <td width="20%" id="noborder"><div  class="STYLE1">发表日期</div></td>
    <td width="10%" id="noborder"><div  class="STYLE1">回复数</div></td>
</tr>
<tr class="yellow">
	<td height="22">aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</td> <td>king</td> <td>a</td> <td>a</td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<td height="22"></td><td></td><td></td><td></td>
</tr>
<tr class="yellow">
	<th colspan="4">翻页</th>
</tr>
 <jsp:include flush="true" page="tail.jsp"></jsp:include>
</table>
        </div>
    </body>
</html>
