package dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import dao.UserDao;
import dbc.BaseDao;

public class UserDaoImpl implements UserDao {
	BaseDao bs = new BaseDao();
	Connection conn = null;
	PreparedStatement pstmt = null;
	ResultSet rs = null;
	
	@Override
	public boolean regUser(String username, String password, String sex) {
		boolean flag = false;
        String sql="insert into users(username,password,sex) values(?,?,?)";
        List<Object> lp = new ArrayList<Object>();
        lp.add(username);
        lp.add(password);
        lp.add(sex);
        flag=bs.update(sql, lp);
		return flag;
	}

	@Override
	public boolean checkUser(String username) {
		boolean flag = true;
		conn=bs.getConnection();
		if(conn!=null)
		{
			String sql = "select * from users where username ='"+username+"'";
			try {
				pstmt=conn.prepareStatement(sql);
				rs=pstmt.executeQuery();
				if(rs.next())
				{
					flag = false;
				}
			} catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return flag;
	}

	@Override
	public String login(String username, String password) {
		String id = null;
		conn=bs.getConnection();
		if(conn!=null)
		{
			String sql = "select*from users where username=? and password=?";
			try {
				pstmt=conn.prepareStatement(sql);
				pstmt.setString(1, username);
				pstmt.setString(2, password);
				rs=pstmt.executeQuery();
				if(rs.next()) 
		           { 
		               id = rs.getString("Id");
		           }
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return id;
	}

	@Override
	public boolean changeUser(String username, String password, String id) {
		boolean flag = true;
		conn=bs.getConnection();
		if(conn!=null)
		{
			String sql = "update users set username=?,password=? where Id=?";
			try {
				pstmt=conn.prepareStatement(sql);
				pstmt.setString(1, username);
				pstmt.setString(2, password);
				pstmt.setString(3, id);
				rs=pstmt.executeQuery();
				if(rs.next())
				{
					flag = false;
				}
			} catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return flag;
	}

	@Override
	public boolean deleteUser(String id) {
		boolean flag = false;
		conn=bs.getConnection();
		if(conn!=null)
		{
			String sql = "delete from users where id ="+id;
			try {
				pstmt=conn.prepareStatement(sql);
				pstmt.executeUpdate();
				flag = true;
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return flag;
	}

}
