package dao.impl;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import bean.Reply;
import dao.ReplyDao;
import dbc.BaseDao;


public class ReplyDaoImpl implements ReplyDao {

	BaseDao bs = new BaseDao();
	Connection conn = null;
	PreparedStatement pstmt = null;
	PreparedStatement pstmtt = null;
	ResultSet rs = null;
	
	@Override
	public boolean addReply(String username, String replyContent, int topicId) {
		boolean flag = false;
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "insert into reply(username,replyContent,topicId)values(?,?,?)";
			String sqll="update topic set replyCount=replyCount+1 where Id="+topicId;
			try {
				pstmt = conn.prepareStatement(sql);
				pstmtt = conn.prepareStatement(sqll);
				pstmt.setString(1,username);
	            pstmt.setString(2,replyContent);
	            pstmt.setInt(3,topicId);
	            pstmt.executeUpdate();
	            pstmtt.executeUpdate();
	            flag = true;
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return flag;
	}

	@Override
	public ArrayList getReplyContentByPage(int pageSize, int currentPage, int topicId) {
		ArrayList al=new ArrayList();
		conn = bs.getConnection();
		if(conn != null)
		{
			String sql = "select * from reply where topicId = "+topicId+" limit "+pageSize*(currentPage-1)+","+pageSize;
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				while(rs.next())
	            {
	                Reply rb = new Reply();
	                rb.setId(rs.getInt(1));
	                rb.setUsername(rs.getString(2));
	                rb.setReplyDate(rs.getString(3));
	                rb.setReplycontent(rs.getInt(4));
	                al.add(rb);
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
		conn=bs.getConnection();
		if(conn!=null)
		{
			String sql = "select count(*) from reply";
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
	public Reply getReplyById(String id) {
		Reply rb = new Reply();
		conn = bs.getConnection();
		if(conn!=null)
		{
			String sql = "select * from reply where topicId="+id;
			try {
				pstmt = conn.prepareStatement(sql);
				rs = pstmt.executeQuery();
				if(rs.next())
	            {
	                rb.setId(rs.getInt(1));
	                rb.setUsername(rs.getString(2));
	                rb.setReplyDate(rs.getString(3));
	                rb.setReplycontent(rs.getInt(4));
	            }
			}catch (SQLException e) {
				e.printStackTrace();
			}finally{
				bs.closeConn(conn, pstmt, rs);
			}
		}
		return rb;
	}

}
