package dbc;

import java.lang.reflect.Field;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class BaseDao {
	
	public Connection getConnection()
	{
		Connection conn = null;
		
		try {
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/web","root","662213");
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return conn;
	}
	
	public void closeConn(Connection conn,PreparedStatement pstmt,ResultSet rs)
	{
		try {
			if(rs!=null)
			{
				rs.close();
			}
			if(pstmt!=null)
			{
				pstmt.close();
			}
			if(conn!=null)
			{
				conn.close();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public boolean update(String sql,List<Object> lp)
	{
		boolean isFlag = false;
		Connection conn = null;
		PreparedStatement pstmt = null;
		ResultSet rs = null;
		conn = getConnection();
		if(conn!=null)
		{
			try {
				pstmt = conn.prepareStatement(sql);
				if(lp.size()>0)
				{
					for(int i = 0;i < lp.size();i++)
					{
						pstmt.setObject(i+1,lp.get(i));
					}
				}
				int num = pstmt.executeUpdate();
				if(num > 0 )
				{
					isFlag = true;
				}
			} catch (SQLException e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			}finally {
				closeConn(conn,pstmt,rs);
			}
		}
		return isFlag;
	}


	public <T>List<T> query(String sql,List<Object> lp,Class clazz)
	{
		List<T> list=new ArrayList<T>();
		Connection conn=null;
		PreparedStatement pstmt=null;
		ResultSet rs=null;
		conn=getConnection();
		if(conn!=null)
		{
			try {
				pstmt=conn.prepareStatement(sql);
				if(lp.size()>0)
				{
					for(int i=0;i<lp.size();i++)
					{
						pstmt.setObject(i+1,lp.get(i));
					}
				}
				rs=pstmt.executeQuery();
				while(rs.next())
				{
					/*
					 * 结果集的第一行存储的列名
					 */
					Object obj=clazz.newInstance();
					ResultSetMetaData rm=rs.getMetaData();//rm对象存储了结果中所有的列名
					int num=rm.getColumnCount();
					for(int i=1;i<=num;i++)
					{
						String name=rm.getColumnName(i);//拿到列名
						Field f=clazz.getDeclaredField(name);
						f.setAccessible(true);
						Object o=rs.getObject(i);
						f.set(obj,o);
					}
					list.add((T) obj);
				}
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (InstantiationException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (NoSuchFieldException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SecurityException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}finally{
				closeConn(conn, pstmt, rs);
			}
		}
		return list;
	}
	
}
