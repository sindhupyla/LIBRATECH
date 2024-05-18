<%@ page import="java.sql.*" %>
<%@ page import="javax.sql.*" %>
<%
String userV=request.getParameter("u_name");
String emailV=request.getParameter("email");

String JDBC_CONNECTION = "com.mysql.jdbc.Driver";
String DB_PATH ="jdbc:mysql://localhost/jdbc_db";

String USER ="root";
String PASS = "Libratech@24" ;

Connection conn=null;
Statement stmt=null;
try{
Class.forName(JDBC_CONNECTION);
conn = DriverManager.getConnection(DB_PATH ,USER,PASS);
stmt=conn.createStatement();
String sql;
sql = "INSERT INTO user_data (username, email) VALUES ('" + userV + "', '" + emailV + "')";
stmt.executeUpdate(sql);
response.sendRedirect("success.jsp?username="+userV);

conn.close();
stmt.close();
}
catch(SQLException se){
se.printStackTrace();
out.println("ERROR :"+se.getMessage());}
catch(Exception e){
e.printStackTrace();
out.println("ERROR :"+e.getMessage());}

try{
if(stmt!=null) stmt.close();}
catch(SQLException e){
e.printStackTrace();
}
try{
if(conn!=null) conn.close();}
catch(SQLException e){
e.printStackTrace();
}
%>
 