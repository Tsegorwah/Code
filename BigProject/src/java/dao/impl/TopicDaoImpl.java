package dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import bean.Topic;
import dao.TopicDao;
import dbc.BaseDao;


public class TopicDaoImpl implements TopicDao {

	BaseDao bs = new BaseDao();
	Connection conn = null;
	PreparedStatement pstmt = null;
	ResultSet rs = null;

	@Override
	public boolean addTopic(String username, String title, String content) {
		boolean flag = false;
		conn = bs.getConnection();
		if(conn != null)
		{
			try {
				String sql = "insert into topic(username,title,content)values(?,?,?)";
				pstmt = conn.prepareStatement(sql);
				pstmt.setString(1, username);
				pstmt.setString(2, title);
				pstmt.setString(3, content);
				pstmt.executeUpdate();
				flag = true;					
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return false;
	}

	@Override
	public ArrayList getTopicByPage(int pageSize, int currentPage) {
		ArrayList al = new ArrayList();
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select * from topic limit  "+pageSize*(currentPage-1)+","+pageSize;
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				while(rs.next())
	            {
	                Topic tb = new Topic();
	                tb.setId(rs.getInt(1));
	                tb.setUsername(rs.getString(2));
	                tb.setTitle(rs.getString(3));
	                tb.setTopicdate(rs.getString(4));
	                tb.setContent(rs.getString(5));
	                tb.setReplycount(rs.getInt(6));
	                al.add(tb);
	            }  
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return al;
	}

	@Override
	public int getRowCount() {
		int rowCount = 0;
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select count(*) from topic";
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				if(rs.next())
					rowCount = rs.getInt(1);
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return rowCount;
	}

	@Override
	public int getReplyCount() {
		int replyCount = 0;
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select count(*) from reply where topicId=1";
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				if(rs.next())
	                replyCount = rs.getInt(1);
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return replyCount;
	}

	@Override
	public Topic getTopicById(String id) {
		Topic tb = new Topic();
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select * from topic where Id="+id;
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				if(rs.next())
	            {
	                tb.setId(rs.getInt(1));
	                tb.setUsername(rs.getString(2));
	                tb.setTitle(rs.getString(3));
	                tb.setTopicdate(rs.getString(4));
	                tb.setContent(rs.getString(5));
	                tb.setReplycount(rs.getInt(6));
	            }
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return null;
	}

	@Override
	public ArrayList getHotReplyByPage(int pageSize, int currentPage) {
		ArrayList al = new ArrayList();
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select * from topic ORDER BY replyCount DESC limit "+pageSize*(currentPage-1)+","+pageSize;
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				while(rs.next())
	            {
	                Topic tb = new Topic();
	                tb.setId(rs.getInt(1));
	                tb.setUsername(rs.getString(2));
	                tb.setTitle(rs.getString(3));
	                tb.setTopicdate(rs.getString(4));
	                tb.setContent(rs.getString(5));
	                tb.setReplycount(rs.getInt(6));
	                al.add(tb);
	            }  
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return al;
	}

	@Override
	public ArrayList getTopicByUsername(String username) {
		ArrayList al = new ArrayList();
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select * from topic where username="+"'"+username+"'";
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				while(rs.next())
	            {
	                Topic tb = new Topic();
	                tb.setId(rs.getInt(1));
	                tb.setUsername(rs.getString(2));
	                tb.setTitle(rs.getString(3));
	                tb.setTopicdate(rs.getString(4));
	                tb.setContent(rs.getString(5));
	                tb.setReplycount(rs.getInt(6));
	                al.add(tb);
	            }  
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return al;
	}

	@Override
	public boolean deleteTopic(String id) {
		boolean flag = false;
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "delete from topic where Id ="+id;
			try {
				pstmt = conn.prepareStatement(sql);
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
