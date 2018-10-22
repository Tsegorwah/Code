<%-- 
    Document   : luntan
    Created on : 2018-10-8, 16:17:12
    Author     : yyznb
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
          <script>
  $(function() {
    $( document ).tooltip();
  });
  </script>
        <div id="lt">
            <table align="center" class="hovertable">
<tr height="120">
    <th colspan="5">  
    <input class="ltbt" type="button" name="Submit" title="发帖" onclick="location.href='reg.jsp'"/>
    <input class="ltbt" type="button" name="Submit" title="查看热力图"  v-on:click="hotblock()"/>
    <input class="ltbt" type="button" name="Submit" title="查看我的贴子" onclick="location.href='reg.jsp'"/>
    <input class="ltbt" type="button" name="Submit2" title="修改个人信息" onclick="location.href='reg.jsp'"/>
    <input class="ltbt" type="button" name="Submit2" title="热帖" onclick="location.href='retie.jsp'"/> 
    
    <div class="city">{{cityname}}论坛</div></th>  
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
	<th colspan="4" height="22">翻页</th>
</tr>
</table>
        </div>
    </body>
</html>
