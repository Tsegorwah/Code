<%-- 
    Document   : map-button
    Created on : 2018-10-2, 14:37:16
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
        <button class="mapbt" @click="getcityname"  onclick="cname(1)" id="1">佛山</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(2)" id="2">广州</button>
        <button class="mapbt" @click="getcityname" onclick="cname(3)" id="3">上海</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(4)" id="4">深圳</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(5)" id="5">沈阳</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(6)" id="6">成都</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(7)" id="7">武汉</button>
        <button class="mapbt" @click="getcityname"  onclick="cname(8)" id="8">北京</button>
    </body>
</html>
